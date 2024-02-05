import numpy as np
import numpy.ma as ma
import sys
from metrics.helper_function import calc_ROI

np.set_printoptions(threshold=sys.maxsize)


def fillrate(ply_files, roi_area=0.6):
    res_list = list()

    assert len(ply_files) > 0, "Should be at least one depth in the list to calculate the fillrate."
    assert ply_files[0].shape[-1] == 3, "Shape should be (h,w,3) numpy array to calculate fill rate."

    for depth in ply_files:
        # get region of interest 
        roi_depth = calc_ROI(depth, roi_area).copy()
        # get only Z values of depth map
        roi_depth = roi_depth[:,:,-1]

        total_size = roi_depth.size
        roi_cut_size = np.sum(~(np.isnan(roi_depth)))


        fill_rate = 100 * roi_cut_size / total_size
        res_list.append(fill_rate)

    if len(res_list) == 0:
        return np.nan

    rms = np.average(res_list)

    return rms
