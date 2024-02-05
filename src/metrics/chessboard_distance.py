import cv2
import numpy as np


def search_neighbors(point_3d,offset_x=0,offset_y=0):
    """Search points, which are the number of the offsets points off.

    Args:
        point_3d (np.array): List of 3D points in the shape of the image. Shape: (width,height,3).
        offset_x (int, optional): Neighbor offset in horizontal direction. Defaults to 0.
        offset_y (int, optional): Neighbor offset in vertical direction. Defaults to 0.

    Returns:
        np.array: Numpy array of distances between neighbor points. Shape (x,)
    """

    assert offset_x != offset_y, "Offset has to be different in x and y direction!"

    distance_list = list()

    for i in range(len(point_3d)-offset_x):
        for j in range(len(point_3d[0])-offset_y):
            point_a = point_3d[i][j]
            point_b = point_3d[i+offset_x][j+offset_y]

            # check for invalid points (all 0. or nan)
            if point_a.all() != 0. and point_b.all() != 0.:
                dist = np.linalg.norm(point_a-point_b)
                distance_list.append(dist)
    
    return distance_list


def calc_mean_distance(point_3d,square_size):
    """ calculate the mean distance of a neighbor points from a chess board

    Args:
        point_3d (np.array): List of 3D points, which are found in the chessboard image.
        square_size (float): Size of the squares for the chessboard

    Returns:
        tuple(3): Mean,standard deviation and length of the distance err.
    """

    distance_list = list()
    # search for horizontal neighbors
    distance_list.extend(search_neighbors(point_3d,offset_x=1))
    # search for vertical neighbors
    distance_list.extend(search_neighbors(point_3d,offset_y=1))

    distance = np.array(distance_list)
    distance_err = np.abs(distance - square_size)

    if len(distance_err) == 0:
        return None,None,0

    return np.mean(distance_err),np.std(distance_err),len(distance_err)
    

def find_3d_points(corners,xyz,chess_shape):
    """ Search for the corresponding valid 3D points of the chessboard corners

    Args:
        corners (list): List of 2D points of the chessboard corners. Shape (chessboard_width,chessboard_height,2)
        xyz (list): List of 3D points of the current scene. Shape (image_width*image_height,3)
        shape (tuple): Width and height of the chessboard pattern.

    Returns:
        tuple: List of valid 2D points and the corresponding valid 3D points.
    """
    point_3d = list()
    for corner in corners:
        pos = (int(corner[1]), int(corner[0]))
        if xyz[pos].all() != 0.:
            point_3d.append(xyz[pos])
        else:
            point_3d.append(np.array([0.,0.,0.]))
                
    # reshape to chessboard size
    point_3d = np.array(point_3d).reshape((chess_shape[1],chess_shape[0],3))

    return point_3d


def compare_distance(pointcloud_list, image_list, square_size=7., chessboard_shape=(8, 10)):
    """ Compute the chessboard-distance error.

    Args:
        pointcloud_list (list): List of numpy-arrays with 3D points of the chessboard. Shape (width,height,3)
        image_list (list): List of images with 2D points of the chessboard. Shape (width,height,2)
        square_size (float): Size of the squares of the chessboard. Default 7.
        chessboard_shape (tuple, optional): Width and height of the chessboard pattern. Defaults to (8, 10).

    Returns:
        tuple(3): Mean, standard deviation and number of chessboard neighbors of the checker distance. Is nothing found then (None,None,None).
    """

    mean_list = list()
    std_list = list()
    num_list = list()

    for xyz, image in zip(pointcloud_list, image_list):
        image_grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret, corners = cv2.findChessboardCorners(image_grey, chessboard_shape, None)
        
        # check 3D points
        if ret:
            corners = corners.squeeze()
            xyz = np.nan_to_num(xyz)
            points_3d = find_3d_points(corners,xyz,chess_shape=chessboard_shape)
            dist_mean,dist_std,num_of_points = calc_mean_distance(points_3d,square_size)
            if dist_mean is not None:
                mean_list.append(dist_mean)
                std_list.append(dist_std)
                num_list.append(num_of_points)
    

    if len(mean_list) > 0:
        return np.mean(mean_list),np.mean(std_list),np.mean(num_list)

    else:
        return None,None,None

