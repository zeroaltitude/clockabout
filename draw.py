#!/usr/local/bin/python3

from PIL import Image, ImageDraw

limit_x = 32
limit_y = 32
im = Image.new("RGB", (limit_x, limit_y), "white")

draw = ImageDraw.Draw(im)
initial_offset_x = 1
initial_offset_y = 1

state = 0
points = [0 for _ in range(60)]
for i in range(15):
    pointq1 = (i * 2 + initial_offset_x, 0)
    pointq2 = (limit_x - 1, i * 2 + initial_offset_y)
    pointq3 = (i * 2 + initial_offset_x, limit_y - 1)
    pointq4 = (0, i * 2 + initial_offset_y)
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


def draw_hand(pos, length=0, color=None):
    center_point = (int(limit_x/2), int(limit_y/2))
    draw.line([center_point, get_coord_for_second(pos)], fill=color)


def draw_second_hand(s):
    draw_hand(s, length=14, color="#ff0000")


def draw_minute_hand(m):
    draw_hand(m, length=12, color="#00ff00")


def draw_hour_hand(s):
    draw_hand(h * 5, length=5, color="#0000ff")


def draw_clock(h, m, s):
    draw_second_hand(s)
    draw_minute_hand(m)
    draw_hour_hand(h)


im.save("foo.png", "PNG")
