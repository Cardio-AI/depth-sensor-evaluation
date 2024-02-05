import pyzed.sl as sl
import numpy as np
import time

import sys,os
# add modules from parent folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metrics.helper_function import filter_by_threshold

def extract_frames(svo_path, depth_mode=sl.DEPTH_MODE.PERFORMANCE, num_frames=1,distance=200.):
    """ extract frames from a svo file as point_cloud or depth map in numpy-array format

    Args:
        svo_path (string): _description_
        camera_offset (float): offset between optical center of the camera and case
        num_frames (int, optional): How many frames should be extract. Defaults to 1.
        distance (float): distance to the target object in mm. Default to 200.

    Returns:
        nd-numpy array: pointcloud shape(height*width,3) or depth map shape(height, width)
    """

    # check if frame numbers valid
    assert num_frames > 0, "number of frames have to greater than 0 and less than max"

    depth_list = list()
    image_list = list()

    # read svo_path
    try:
        # Create pipeline
        init = sl.InitParameters()
        init.set_from_svo_file(str(svo_path))
        init.svo_real_time_mode = False  # Don't convert in realtime

        # change the coordinate system to look at the front of the object
        init.coordinate_units = sl.UNIT.MILLIMETER
        init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

        # clap the current depth values for point cloud visibility
        init.depth_minimum_distance = 0. # all near values are valid
        init.depth_maximum_distance = 1000. # 1 meter distance
        init.depth_mode = depth_mode
        cam = sl.Camera()

        status = cam.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            sys.exit(1)
            

        nb_frames = cam.get_svo_number_of_frames()
        assert num_frames <= nb_frames, "The file has only " + \
            str(nb_frames)+" frames"

        runtime = sl.RuntimeParameters()
        runtime.confidence_threshold = 100
        runtime.texture_confidence_threshold = 100
        # number of frames in the recording
        frame_num = 0  # counter for saved frames
        skipped_frames = 15

        sl_depth = sl.Mat()
        sl_image = sl.Mat()

        while True:
            # Streaming loop
            # skip the first x frame because of auto exposure is set up
            if cam.get_svo_position() <= skipped_frames:
                cam.set_svo_position(skipped_frames)
            
            if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
                # Get the left image
                cam.retrieve_image(sl_image, sl.VIEW.LEFT)
                image = np.asarray(sl_image.get_data()).copy()

                # Get depth information
                cam.retrieve_measure(sl_depth, sl.MEASURE.XYZRGBA)
                # reshape to (n,3) -> x,y,z to save it as .ply
                np_depth = np.asarray(sl_depth.get_data()).copy()
                np_depth = np_depth[:, :, :3]
                # change all invalid values to 0.
                np_depth[np_depth== -np.inf] = np.nan
                np_depth[np_depth== np.inf] = np.nan

                depth = filter_by_threshold(np_depth,distance-20,distance+20)
                image_list.append(image)
                depth_list.append(depth)
                frame_num += 1
                # check is the number of frames are reached, note that 10 frames are skipped
                if frame_num >= num_frames:
                    break

        cam.close()
        return depth_list, image_list
                
    except Exception as e:
        print(e)
    finally:
        cam.close()
        del cam
        time.sleep(0.1)

