import numpy as np


def rotate_points(points, angle):
    angle_rad = np.deg2rad(angle)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                [np.sin(angle_rad), np.cos(angle_rad)]])

    rotated_points = np.dot(points, rotation_matrix)
    return rotated_points


def phi(x0, y0, x1, y1, l, alpha, k, t):
    return k * t * (np.log(abs(r(x0, x1, y0, y1, 1, l + x0, y0, -alpha) + l + x0 - rotate_points([x1, y1], -alpha)[0]))
                    - np.log(abs(r(x0, x1, y0, y1, 1, x0, y0, -alpha) + x0 - rotate_points([x1, y1], -alpha)[0]))
                    + np.log(
                abs(r(x0, x1, y0, y1, 2, x0, l + y0, -alpha) + l + y0 - rotate_points([x1, y1], -alpha)[1]))
                    - np.log(abs(r(x0, x1, y0, y1, 2, x0, y0, -alpha) + y0 - rotate_points([x1, y1], -alpha)[1])))


def r(x0, x1, y0, y1, num, x, y, alpha):
    if num == 1:
        return np.sqrt((x - rotate_points([x1, y1], alpha)[0]) ** 2 + (rotate_points([x1, y1], alpha)[1] - y0) ** 2)
    else:
        return np.sqrt((y - rotate_points([x1, y1], alpha)[1]) ** 2 + (rotate_points([x1, y1], alpha)[0] - x0) ** 2)
