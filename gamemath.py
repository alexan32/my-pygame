import math
import pygame

def degrees_between_two_points(a, b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    return math.degrees(math.atan2(y, x))

def radians_between_two_points(a, b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    return math.atan2(y, x)

def distance_between_two_points(a, b):
    return math.sqrt(math.pow(b[0]-a[0], 2) + math.pow(b[1]-a[1], 2))

def get_xy_move(angle):
    return math.cos(angle), math.sin(angle)

# where AB is a line segment, and P is a point
def closest_point_on_segment(P, A, B):
    v = (B[0] - A[0], B[1] - A[1])
    u = (A[0] - P[0], A[1] - P[1])
    vu = v[0] * u[0] + v[1] * u[1]
    vv = v[0] ** 2 + v[1] ** 2
    t = -vu / vv
    if t < 0:
        t = 0
    elif t > 1:
        t = 1
    return A[0] + t*v[0], A[1] + t*v[1]

def closest_point_in_rectangle(P, rect):
    horiz = P[0] < rect.center[0]
    vert = P[1] < rect.center[1]
    if horiz:
        if vert:
            seg1 = (rect.bottomleft, rect.topleft)
            seg2 = (rect.topleft, rect.topright)
        else:
            seg1 = (rect.bottomleft, rect.topleft)
            seg2 = (rect.bottomleft, rect.bottomright)
    else:
        if vert:
            seg1 = (rect.topleft, rect.topright)
            seg2 = (rect.topright, rect.bottomright)
        else:
            seg1 = (rect.bottomright, rect.topright)
            seg2 = (rect.bottomleft, rect.bottomright)
    P1 = closest_point_on_segment(P, seg1[0], seg1[1])
    P2 = closest_point_on_segment(P, seg2[0], seg2[1])
    if distance_between_two_points(P, P1) < distance_between_two_points(P, P2):
        return P1
    return P2
