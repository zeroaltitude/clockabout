#!/usr/local/bin/python3

import math

from PIL import Image, ImageDraw


limit_x = 36
limit_y = 36
abs_offset_x = 2
abs_offset_y = 2
# real_width = limit_x - (2 * abs_offset_x)
# real_height = limit_y - (2 * abs_offset_y)
im = Image.new("RGB", (limit_x, limit_y), "white")

draw = ImageDraw.Draw(im)
initial_offset_x = 1
initial_offset_y = 1

center_point = (int(limit_x / 2) - 1, int(limit_y / 2) - 1)

state = 0
points = [0 for _ in range(60)]
for i in range(15):
    pointq1 = (i * 2 + initial_offset_x + abs_offset_x, 0 + abs_offset_y)
    pointq2 = (limit_x - 1 - abs_offset_x, i * 2 + initial_offset_y + abs_offset_y)
    pointq3 = (i * 2 + initial_offset_x + abs_offset_x, limit_y - 1 - abs_offset_y)
    pointq4 = (0 + abs_offset_x, i * 2 + initial_offset_y + abs_offset_y)
    draw.point([pointq1, pointq2, pointq3, pointq4], fill="black")
    points[i] = pointq1
    points[i + 15] = pointq2
    points[44 - i] = pointq3
    points[59 - i] = pointq4


def get_coord_for_second(s):
    # simple: index into points with offset
    offset = 7
    seconds = 60
    return points[(s + offset) % seconds]


# colorize the 5 points
for j in range(0, 60, 5):
    c = get_coord_for_second(j)
    draw.point(c, fill="blue")
    if c[0] == 0 + abs_offset_x:
        draw.point([c[0] + 1, c[1]], fill="blue")
    elif c[0] == limit_x - 1 - abs_offset_x:
        draw.point([c[0] - 1, c[1]], fill="blue")
    elif c[1] == 0 + abs_offset_y:
        draw.point([c[0], c[1] + 1], fill="blue")
    elif c[1] == limit_y - 1 - abs_offset_y:
        draw.point([c[0], c[1] - 1], fill="blue")


def draw_hand(pos, length=0, color=None):
    dest_point = get_coord_for_second(pos)
    if center_point[0] == dest_point[0]:
        # infinite slope, simply alter y
        if dest_point[1] == 0 + abs_offset_y:
            dest_point = (dest_point[0], center_point[1] - length)
        else:
            dest_point = (dest_point[0], center_point[1] + length)
    elif center_point[1] == dest_point[1]:
        # zero slope, simply alter x
        if dest_point[0] == 0 + abs_offset_x:
            dest_point = (center_point[0] - length, dest_point[1])
        else:
            dest_point = (center_point[0] + length, dest_point[1])
    else:
        # slope
        slope = (dest_point[1] - center_point[1]) / (dest_point[0] - center_point[0])
        # solve for length: x**2 + y**2 = length
        # y = mx
        # (1 + m**2)x**2 = length**2
        xcoord = math.sqrt((length ** 2) / (1 + (slope ** 2)))
        ycoord = slope * xcoord
        xmathmod = math.ceil
        ymathmod = math.ceil
        if pos > 30:
            # 3rd and 4th quadrants: reverse the coord modifier
            xcoord = xcoord * -1.
            ycoord = ycoord * -1.
        if xcoord > 0 and ycoord > 0:
            xmathmod = math.floor
        elif xcoord < 0 and ycoord < 0:
            ymathmod = math.floor
        elif xcoord > 0 and ycoord < 0:
            pass
        elif xcoord < 0 and ycoord > 0:
            ymathmod = math.floor
        dest_point = (center_point[0] + xmathmod(xcoord), center_point[1] + ymathmod(ycoord))
    draw.line([center_point, dest_point], fill=color)


def draw_second_hand(s):
    draw_hand(s, length=17, color="#ff0000")


def draw_minute_hand(m):
    draw_hand(m, length=15, color="#000000")


def draw_hour_hand(h):
    draw_hand(h * 5, length=10, color="#000000")


def draw_clock(h, m, s):
    draw_second_hand(s)
    draw_minute_hand(m)
    draw_hour_hand(h)


draw_clock(1, 9, 13)
#draw_clock(3, 30, 45)
#draw_clock(4, 25, 29)
#draw_clock(7, 40, 44)
#draw_clock(10, 55, 59)
#draw_clock(10, 37, 31)
im.save("foo.png", "PNG")
