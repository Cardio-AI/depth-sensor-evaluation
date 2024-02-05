import numpy as np
import sys
from sklearn.metrics import mean_squared_error

from metrics.helper_function import calc_ROI
np.set_printoptions(threshold=sys.maxsize)

def subPixErr(img,b=54.987):
    data = img
    data = calc_ROI(data, 0.4)
    y, x = data.shape
    f = 1 / 2 * (x / np.tan(68.1 / 2))

    plane = planeFit(data)
    plane = np.ndarray.flatten(plane[0])

    data = np.ndarray.flatten(data)
    err = 0
    c = 0
    rms = -1
    for i in data:
        if i > 0:
            d_i = b * f / i
            # err = err + d_i * d_i
            d_ip = b * f / plane[int(i / x)]
            err = err + pow(d_i - d_ip, 2)
            c = c + 1
    if c != 0:
        rms = np.sqrt(err / c)

    return rms


def planeFit(points):
    """
    p, n = planeFit(points)

    Given an array, points, of shape (d,...)
    representing points in d-dimensional space,
    fit an d-dimensional plane to the points.
    Return a point, p, on the plane (the point-cloud centroid),
    and the normal, n.
    """
    import numpy as np
    from numpy.linalg import svd
    points = np.reshape(points, (np.shape(points)[0], -1))  # Collapse trialing dimensions
    assert points.shape[0] <= points.shape[1], "There are only {} points in {} dimensions.".format(points.shape[1],
                                                                                                   points.shape[0])
    ctr = points.mean(axis=1)
    x = points - ctr[:, np.newaxis]
    M = np.dot(x, x.T)  # Could also use np.cov(x) here.
    return ctr, svd(M)[0][:, -1]
