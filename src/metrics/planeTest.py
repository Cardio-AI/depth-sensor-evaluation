import numpy as np
from numpy.linalg import svd
import sys

from metrics.helper_function import calc_ROI, remove_invalid_values
np.set_printoptions(threshold=sys.maxsize)


def get_Z_accuracy(ply_files, GT, roi_area=0.6):
    res_list = list()
    for depth in ply_files:
        # get region of interest 
        roi_depth = calc_ROI(depth, roi_area)
        # reshape to (n,3)
        roi_depth = roi_depth.reshape(-1,3)
        # all invalid values
        roi_depth = remove_invalid_values(roi_depth)

        plane = plane_from_points(roi_depth)
        err = abs(abs(GT) - abs(plane[-1]))

        res_list.append(err)

    if len(res_list) == 0:
        return np.nan

    rms = np.average(res_list)
    return rms


# Define a function to fit a plane to the points
def plane_fit(points:np.array):
    mean = np.mean(points, axis=0)
    points = points - mean
    
    # Compute the covariance matrix of the points
    cov = np.cov(points.T)
    # Perform singular value decomposition on the covariance matrix
    u, s, v = np.linalg.svd(cov)
    # The normal vector of the plane is the last column of v
    normal = v[:, -1]
    # The equation of the plane is ax + by + cz = d
    # where [a, b, c] is the normal vector and d is the dot product of the mean and the normal
    d = np.dot(mean, normal)
    # Return the coefficients of the plane equation
    return normal[0], normal[1], normal[2], d
    

def plane_from_points(points:np.array):
    # Based on: https://github.com/IntelRealSense/librealsense/blob/8ffb17b027e100c2a14fa21f01f97a1921ec1e1b/tools/depth-quality/depth-metrics.h#L70
    # Based on: http://www.ilikebigbits.com/blog/2015/3/2/plane-from-points
    if points.shape[-1] != 3:
        return None

    centroid = np.mean(points,axis=0)

    # Calc full 3x3 covariance matrix, excluding symmetries:
    xx = 0.0; xy = 0.0; xz = 0.0
    yy = 0.0; yz = 0.0; zz= 0.0

    for p in points:
        r = p - centroid

        xx += r[0] * r[0]
        xy += r[0] * r[1]
        xz += r[0] * r[2]
        yy += r[1] * r[1]
        yz += r[1] * r[2]
        zz += r[2] * r[2]
    
    det_x = yy*zz - yz*yz
    det_y = xx*zz - xz*xz
    det_z = xx*yy - xy*xy

    det_max = max(det_x, det_y, det_z)
    if det_max <= 0.0:
        return 0,0,0,0; # The points don't span a plane
    
    dir = 0
    if det_max == det_x:
        a = (xz*yz - xy*zz) / det_x
        b = (xy*yz - xz*yy) / det_x
        dir = np.array([1,a,b])
    elif det_max == det_y:
        a = (yz*xz* -xy*zz) /det_y
        b = (xy*xz -yz*xx) /det_y
        dir = np.array([a,1,b])
    else:
        a = (yz*xy -xz*yy)/det_z
        b = (xz*xz -yz*xx)/det_z
        dir = np.array([a,b,1])

    dir_norm = dir / np.linalg.norm(dir)
    d =  np.dot(centroid, dir_norm)
    plane = dir_norm[0], dir_norm[1], dir_norm[2], d
    return plane

