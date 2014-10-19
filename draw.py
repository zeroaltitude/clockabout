#!/usr/local/bin/python3

import math

from PIL import Image, ImageDraw


scale = 1
limit_x = 36 * scale
limit_y = 36 * scale
abs_offset_x = 2 * scale
abs_offset_y = 2 * scale
initial_offset_x = 1 * scale
initial_offset_y = 1 * scale
center_point = (int(limit_x / 2) - scale, int(limit_y / 2) - scale)
points = [0 for _ in range(60)]


def get_coord_for_second(s):
    # simple: index into points with offset
    offset = 7
    seconds = 60
    return points[(s + offset) % seconds]


def draw_face(draw):
    global points
    state = 0
    for i in range(15):
        pointq1 = (i * (2 * scale) + initial_offset_x + abs_offset_x, 0 + abs_offset_y)
        pointq2 = (limit_x - scale - abs_offset_x, i * (2 * scale) + initial_offset_y + abs_offset_y)
        pointq3 = (i * (2 * scale) + initial_offset_x + abs_offset_x, limit_y - scale - abs_offset_y)
        pointq4 = (0 + abs_offset_x, i * (2 * scale) + initial_offset_y + abs_offset_y)
        draw.point([pointq1, pointq2, pointq3, pointq4], fill="black")
        points[i] = pointq1
        points[i + 15] = pointq2
        points[44 - i] = pointq3
        points[59 - i] = pointq4

    # colorize the hour points
    for j in range(0, 60, 5):
        c = get_coord_for_second(j)
        draw.point(c, fill="blue")
        if c[0] == 0 + abs_offset_x:
            draw.line([(c[0], c[1]), (c[0] + scale, c[1])], fill="blue")
        elif c[0] == limit_x - scale - abs_offset_x:
            draw.line([(c[0], c[1]), (c[0] - scale, c[1])], fill="blue")
        elif c[1] == 0 + abs_offset_y:
            draw.line([(c[0], c[1]), (c[0], c[1] + scale)], fill="blue")
        elif c[1] == limit_y - scale - abs_offset_y:
            draw.line([(c[0], c[1]), (c[0], c[1] - scale)], fill="blue")


def draw_hand(draw, pos, length=0, color=None):
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


def draw_second_hand(draw, s):
    draw_hand(draw, s, length=17 * scale, color="#ff0000")


def draw_minute_hand(draw, m):
    draw_hand(draw, m, length=15 * scale, color="#000000")


def draw_hour_hand(draw, h):
    draw_hand(draw, h * 5, length=10 * scale, color="#000000")


def draw_clock(word, h, m, s):
    im = Image.new("RGBA", (limit_x, limit_y), "white")
    trans = [(255, 255, 255, 0) for _ in range(limit_y * limit_x)]
    im.putdata(trans)
    draw = ImageDraw.Draw(im)
    draw_face(draw)
    draw_second_hand(draw, s)
    draw_minute_hand(draw, m)
    draw_hour_hand(draw, h)
    im.save("png/%s.png" % word, "PNG")


if __name__ == "__main__":
    draw_clock("test", 1, 9, 13)
    #draw_clock("test", 3, 30, 45)
    #draw_clock("test", 4, 25, 29)
    #draw_clock("test", 7, 40, 44)
    #draw_clock("test", 10, 55, 59)
    #draw_clock("test", 10, 37, 31)
