import numpy as np
import json
import pyrealsense2 as rs



def calc_ROI(img, roi_fac):
    """ Calculate a ROI from the image center (border are cropped)

    Args:
        img (np.array): Image matrix of as np.array
        roi_fac (float): scaling factor of the ROI. 

    Returns:
        np.array: Return a border cropped version of the image
    """
    image = img.copy()
    h, w = img.shape[:2]
    w_x1 = int(w / 2 - w / 2 * roi_fac)
    w_x2 = int(w / 2 + w / 2 * roi_fac)
    h_y1 = int(h / 2 - h / 2 * roi_fac)
    h_y2 = int(h / 2 + h / 2 * roi_fac)
    
    return image[h_y1:h_y2, w_x1:w_x2]


def cleanUp_outlier(data, lower_bound=5, upper_bound=95):
    data = np.absolute(data)
    data = data[data > 0]  # remove unvalid pixel
    if len(data) == 0:
        return data
    p_lower = np.percentile(data, lower_bound)
    p_upper = np.percentile(data, upper_bound)
    data = data[data <= p_upper]  # remove 5 Perecnitel
    data = data[data >= p_lower]  # remove 95 pecentile

    return data

def remove_invalid_values(points,remove_nan=True,remove_zero=True):
    assert points.shape[-1] == 3, "Wrong shape of point to filter invalid values! Should be (n,3)"
    if remove_nan:
        points = points[~np.isnan(points).any(axis=1)]
    if remove_zero:
        points = points[~np.all(points==0.,axis=1)]
    
    return points


def filter_by_threshold(np_array, min, max):
    depth_data = np_array.copy()
    nan_values = np_array.copy()
    
    if len(depth_data.shape) == 2:
        nan_values[np_array[:,-1] == 0.] = np.nan
        depth_data[(np.abs(np_array[:,-1]) <= min)] = 0.
        depth_data[(np.abs(np_array[:,-1]) >= max)] = 0.
    elif len(depth_data.shape) == 3:
        depth_data[np_array[:,:,-1]==0.] = np.nan
        depth_data[(np.abs(np_array[:,:,-1]) <= min)] = 0.
        depth_data[(np.abs(np_array[:,:,-1]) >= max)] = 0.

    depth_data[np.isnan(nan_values)] = np.nan

    return depth_data

def read_json(path):
    json_file = open(path)
    json_str = json_file.read()
    json_file.close()
    return json.loads(json_str)

def get_intel_filter(names):
    filter_list = list()
    if names is None:
        return filter_list
    
    for name in names:
        if name == "decimation_filter":
            filter_list.append(rs.decimation_filter())
        if name == "spatial_filter":
            filter_list.append(rs.spatial_filter()) 
        if name == "temporal_filter":
            filter_list.append(rs.temporal_filter()) 
        if name == "hole_filling_filter":
            filter_list.append(rs.hole_filling_filter())

    return filter_list