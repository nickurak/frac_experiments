#!/usr/bin/env python3
import sys
import random
from math import cos, sin, radians

import pygame
from pygame.locals import FULLSCREEN, DOUBLEBUF, KEYDOWN, K_ESCAPE, K_q, K_SPACE

random.seed()
pygame.init()

profiling = True

frameskip = 5000
#create the screen

infoObject = pygame.display.Info()

width = infoObject.current_w
height = infoObject.current_h

width = min(width, height)
height = min(height, width)

mhw = min(height, width)

fh = mhw - 20
# fh = (4.0/3.0) * 0.86602540378 * w
w = fh / (4.0/3.0) / 0.86602540378

paused = False

def rotate2d(degrees, point, origin):
    """
    A rotation function that rotates a point around a point
    to rotate around the origin use [0,0]
    """
    x = point[0] - origin[0]
    yorz = point[1] - origin[1]
    newx = (x*cos(radians(degrees))) - (yorz*sin(radians(degrees)))
    newyorz = (x*sin(radians(degrees))) + (yorz*cos(radians(degrees)))
    newx += origin[0]
    newyorz += origin[1]

    return newx, newyorz

def maxsep(p1, p2, p3):
    top = 0
    top = max(top, abs(p1[0] - p2[0]))
    top = max(top, abs(p2[0] - p3[0]))
    top = max(top, abs(p3[0] - p1[0]))
    top = max(top, abs(p1[1] - p2[1]))
    top = max(top, abs(p2[1] - p3[1]))
    top = max(top, abs(p3[1] - p1[1]))
    return top


ip1 = (10, fh / 4.0 + 10)
ip2 = (w+10, fh / 4.0 + 10)
ip3 = rotate2d(60, ip2, ip1)

initsep = maxsep(ip1, ip2, ip3)

def end_frac():
    pygame.quit()
    sys.exit()

def handle_events():
    global paused
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_frac()
            elif event.type == KEYDOWN:
                if event.key in [K_ESCAPE, K_q]:
                    end_frac()
                if event.key == K_SPACE:
                    paused = not paused
                elif event.type == KEYDOWN and event.key == K_q:
                    end_frac()
        if not paused:
            break
        pygame.time.wait(10)

flags = FULLSCREEN | DOUBLEBUF
window = pygame.display.set_mode((width, height), flags, 16)

def mix(a, b, r):
    return (a[0] / r + b[0] * (r-1) / r, a[1] / r + b[1] * (r-1) / r)



lenranfactor = 0.005
rotranfactor = 10
lenranfactor = 0.0
rotranfactor = 0


i = 0

sierpstack = []

def sierp(a, b, c, color):
    global i
    p1 = mix(a, b, 2)
    p2 = mix(b, c, 2)
    p3 = mix(c, a, 2)

    pygame.draw.line(window, color, p1, p2)
    pygame.draw.line(window, color, p2, p3)
    pygame.draw.line(window, color, p3, p1)
    i = i + 1
    if i == frameskip:
        pygame.display.flip()
        i = 0
        handle_events()
    sep = maxsep(p1, p2, p3)
    if sep > 6:
        color2 = (color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
        koch(p3, p2, color2)
        koch(p1, p3, color2)
        koch(p2, p1, color2)

        color3 = (color[0] * 0.7, color[1], color[2])
        sierpstack.append((a, p1, p3, color3))
        color3 = (color[0], color[1] * 0.7, color[2])
        sierpstack.append((b, p2, p1, color3))
        color3 = (color[0], color[1], color[2] * 0.7)
        sierpstack.append((c, p3, p2, color3))

def koch(start, end, color):
    global i
    p1 = mix(end, start, 3)
    p3 = mix(start, end, 3)
    p2 = rotate2d(-60, p3, p1)
    sep = maxsep(p1, p2, p3)
    if sep > 1:
        color2 = (color[0], color[1] * 0.75, color[2])
        color = (color[0]*0.75, color[1], color[2])
        koch(start, p1, color)
        koch(p1, p2, color2)
        koch(p2, p3, color2)
        koch(p3, end, color)
    else:
        pygame.draw.line(window, color, start, end)
        i = i + 1
        if i == frameskip:
            pygame.display.flip()
            i = 0
            handle_events()
    if sep > 6:
        color2 = (color2[0] * 0.5, color2[1] * 0.5, color2[2] * 0.5)
        sierpstack.append((p1, p2, p3, color2))


def maindraw():
    koch(ip1, ip2, (255, 255, 255))
    koch(ip2, ip3, (255, 255, 255))
    koch(ip3, ip1, (255, 255, 255))

    koch(ip2, ip1, (255, 255, 255))
    koch(ip3, ip2, (255, 255, 255))
    koch(ip1, ip3, (255, 255, 255))

    print(len(sierpstack))
    while sierpstack:
        params = sierpstack.pop(0)
        sierp(params[0], params[1], params[2], params[3])

    pygame.display.flip()
    pygame.display.flip()

if not profiling:
    maindraw()
else:
    import cProfile
    import pstats
    cProfile.run('maindraw()', 'restats')

    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats('tottime').print_stats()
    p.strip_dirs().sort_stats('cumulative').print_stats()

while True:
    handle_events()
    pygame.time.wait(10)
