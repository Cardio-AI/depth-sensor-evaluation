import numpy as np
import sys
from metrics.helper_function import calc_ROI

np.set_printoptions(threshold=sys.maxsize)


def get_tempNoise(images, roi_fac=0.6):
    try:
        # filter to z-values (n,h,w,xyz)
        data = np.array(images)[:,:,:,-1]
        # convert filtered values to numeric
        data = np.nan_to_num(data)
        # remove invalid values
        data = np.ma.masked_equal(data,0)

        # calculate standard deviation the mats
        std_matrix = np.std(data,0)
        # use only the region of interest for the metric
        ROI_mat = calc_ROI(std_matrix,roi_fac)
        med_avr = np.average(ROI_mat)
    except Exception as e:
        print(e)
        med_avr = np.nan

    return med_avr
