import pyrealsense2 as rs
import numpy as np
import sys,os
import cv2 

# add modules from parent folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metrics.helper_function import filter_by_threshold, read_json

from scipy.spatial.transform import Rotation
from metrics.helper_function import get_intel_filter


def extract_frames(bag_path,post_processes_names=None, num_frames=1,distance=200.):
    """ extract frames from a svo file as point_cloud or depth map in numpy-array format

    Args:
        bag_path (string): _description_
        camera_offset (float): offset between optical center of the camera and case
        post_processes (list, optional): Defaults to None.
        num_frames (int, optional): How many frames should be extract. Defaults to 1.
        distance (float): distance of the target object in mm. Default to 200.

    Returns:
        nd-numpy array: pointcloud shape(height*width,3) or depth map shape(height, width)
    """

    # check if frame numbers valid
    assert num_frames > 0, "number of frames have to greater than 0 and less than max"

    depth_list = list()
    image_list = list()

    file_configs = read_json(bag_path.split('.')[0]+".json")
    fps = int(file_configs["viewer"]["stream-fps"])
    filters = get_intel_filter(post_processes_names)
    # read bag_path
    try:
        # Create pipeline
        pipeline = rs.pipeline()
        config = rs.config()
        rs.config.enable_device_from_file(config, bag_path)

        config.enable_stream(rs.stream.depth, rs.format.z16,fps)
        config.enable_stream(rs.stream.color)

        align = rs.align(rs.stream.color)

        # Start streaming from file
        pipeline.start(config)

        # create intel_point cloud obj
        pcd_intel = rs.pointcloud()
        frame_num = 0  # counter for saved frames
        skipped_frames = 5

        # Streaming loop
        while True:
            # skip the first x frame because of auto exposure is set up
            frame_num += 1
            if frame_num < skipped_frames:
                continue

            # Get frameset of depth
            frames = pipeline.wait_for_frames()

            if frames.size() <2:
                print("Not enough frames for alignment")
                continue

            align_frames = align.process(frames)
            # Get depth frame
            depth_frame = align_frames.get_depth_frame()
            color_frame = align_frames.get_color_frame()
            image = np.asarray(color_frame.get_data())
            # Use postprocessing filters
            if filters:
                for filter in filters:
                    depth_frame = filter.process(depth_frame)
                # check if the decimation_filter is used, and change image size according to the new depth size        
                if "decimation_filter" in post_processes_names:
                    image = cv2.resize(image,(int(image.shape[1]/2),int(image.shape[0]/2)))

            image_shape = image.shape[:2] # get image dimensions
            # extract pointcloud
            pcd_points = pcd_intel.calculate(depth_frame)
            np_depth = np.asanyarray(pcd_points.get_vertices())
            np_depth = np.array([list(xyz) for xyz in np_depth], dtype=np.float32)
            np_depth = np_depth  * 1000  # convert meter to mm

            # change rotation to look at the front
            r = Rotation.from_euler('x',180,degrees=True)
            np_depth = np_depth @ r.as_matrix()
                  
            np_depth = filter_by_threshold(np_depth,distance-20,distance+20)

            np_depth = np_depth.reshape(image_shape+(3,))

            depth_list.append(np_depth)
            image_list.append(image)
            # check is the number of frames are reached, note that 10 frames are skipped
            if frame_num - skipped_frames - num_frames >= -1:
                return depth_list,image_list
    finally:
        # TODO file release only if it opened
        pipeline.stop()
        pass
    
