import numpy as np
import matplotlib as plt
import os
import subprocess
import sys
import time
import math
from coordinate import Coordinate2D


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


# Euclidean distance
def calc_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# Average
def calc_avg_pos(center_point_1, center_point_2, intersection_point):
    return ((center_point_1.x + center_point_2.x + intersection_point.x) / 3,
            (center_point_1.y + center_point_2.y + intersection_point.y) / 3)


# param : ap1, ar2 = data dictionary
def ap_circle_condition_check(ap1, ap2):
    dist = calc_dist((ap1['x'], ap1['y']), (ap2['x'], ap2['y']))  # distance of the two circles
    radius_1 = ap1['dist']  # AP_1's radius
    radius_2 = ap2['dist']  # AP_2 's radius

    # inner circle check(one circle is inside the other)
    if dist < abs(radius_1 - radius_2):
        return False
    # if radius_1 > dist or radius_2 > dist: # partial inner
    #     return False

    # separate circle check
    if dist > radius_1 + radius_2:
        return False

    # coincide circle check
    if dist == 0 and radius_1 == radius_2:
        return False

    return True


# param : ap1, ar2 = data dictionary
def get_intersecting_points(ap1, ap2):
    if ap_circle_condition_check(ap1, ap2) == False:
        print 'skip_checking since the circle does not qualify'
        # skip the test
    else:
        dist = calc_dist((ap1['x'], ap1['y']), (ap2['x'], ap2['y']))  # distance of the two circles
        radius_1 = ap1['dist']  # AP_1's radius
        radius_2 = ap2['dist']  # AP_2 's radius

        sub_x = ap2['x'] - ap1['x']
        sub_y = ap2['y'] - ap1['y']
        tmp = (radius_1 * radius_1 - radius_2 * radius_2 + dist * dist) / (2 * dist)
        tmp_2 = math.sqrt(radius_1 * radius_1 - tmp * tmp)
        xm = ap1['x'] + tmp * sub_x / dist
        ym = ap1['y'] + tmp * sub_y / dist
        pt_x1 = xm + tmp_2 * sub_y / dist
        pt_x2 = xm - tmp_2 * sub_y / dist
        pt_y1 = ym - tmp_2 * sub_x / dist
        pt_y2 = ym + tmp_2 * sub_x / dist

    return (pt_x1, pt_y1), (pt_x2, pt_y2)


if __name__ == "__main__":

    ap1 = {'dist': 4, 'x': 0, 'y': 0}
    ap2 = {'dist': 2, 'x': 3, 'y': 0}
    L1 = line((ap1['x'], ap1['y']), (ap2['x'], ap2['y']))
    L2 = line([-5, 1], [5, 1])

    intersect_point_1, intersect_point_2 = get_intersecting_points(ap1, ap2)
    ap_center_line = line((ap1['x'], ap1['y']), (ap2['x'], ap2['y']))
    intersect_point_line = line(intersect_point_1, intersect_point_2)
    intersection_centroid = (0.0, 0.0)
    # intersecting in only one point
    if intersect_point_1 == intersect_point_2:
        intersection_centroid = intersect_point_1
    else:
        intersection_centroid = intersection(ap_center_line, intersect_point_line)
    if intersection_centroid:
        print "Intersection detected:", intersection_centroid
    print (ap1['x'], ap1['y'])
    print (ap2['x'], ap2['y'])

    res = calc_avg_pos(Coordinate2D((ap1['x'], ap1['y'])), Coordinate2D((ap2['x'], ap2['y'])),
                       Coordinate2D(intersection_centroid))
    print("X: %.4f, Y:%.4f" % (res[0], res[1]))
