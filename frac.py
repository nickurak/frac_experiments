#!/usr/bin/env python
import sys
import pygame
import random

random.seed()
pygame.init() 


frameskip = 5000
#create the screen

width = 1920
height = 1080

width = min(width, height)
height = min(height, width)

def end():
    pygame.quit()
    sys.exit()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            end()
        elif event.type == KEYDOWN and event.key == K_q:
            end()

from pygame.locals import *
flags = FULLSCREEN | DOUBLEBUF
window = pygame.display.set_mode((width, height), flags, 16)

def mix(a, b, r):
    return (a[0] * r + b[0] * (1-r), a[1] * r + b[1] * (1-r))

from math import * 

def rotate2d(degrees,point,origin):
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

    return newx,newyorz

lenranfactor=0.005
rotranfactor=10
lenranfactor=0.0
rotranfactor=0


i = 0

def maxsep(*points):
    m = 0
    for p1 in points:
        for p2 in points:
            m = max(m, abs(p1[0] - p2[0]))
    return m

def sierp(a, b, c, color):
    global i
    p1=mix(a, b, 0.5)
    p2=mix(b, c, 0.5)
    p3=mix(c, a, 0.5)

    pygame.draw.line(window, color, p1, p2)
    pygame.draw.line(window, color, p2, p3)
    pygame.draw.line(window, color, p3, p1)
    i = i + 1
    if (i == frameskip):
        pygame.display.flip() 
        i = 0
        handle_events()
    mindif = 6
    sep = maxsep(p1, p2, p3)
    if sep > mindif:
        color2 = (255 * float(sep)/height, 255 * float(sep)/height, 255 * float(sep) / height)
        sierp(p1, p2, p3, color2)
        color3 = (color[0] * 0.5, color[1], color[2])
        sierp(a, p1, p3, color3)
        color3 = (color[0], color[1] * 0.5, color[2])
        sierp(p1, b, p2, color3)
        color3 = (color[0], color[1], color[2] * 0.5)
        sierp(p3, p2, c, color3)

def koch(start, end, color):
    global i
    p1 = mix(start, end, 2.0/3)
    p3 = mix(start, end, 1.0/3) 
    p2 = rotate2d(-60, p3, p1)
    mindif = 1
    sep = maxsep(p1, p2, p3)
    if sep > mindif:
        color2 = (color[0], color[1] * 0.5, color[2])
        color = (color[0], color[1], color[2] * 0.5)
        koch(start, p1, color)
        koch(p1, p2, color2)
        koch(p2, p3, color2)
        sierp(p1, p2, p3, color2)
        koch(p3, end, color)
    else:
        pygame.draw.line(window, color, start, end)
        i = i + 1
        if (i == frameskip):
            pygame.display.flip() 
            i = 0
            handle_events()

mhw = min(height, width)

fh = mhw - 20
# fh = (4.0/3.0) * 0.86602540378 * w
w = fh / (4.0/3.0) / 0.86602540378



p1=(10, fh / 4.0 + 10)
p2=(w+10, fh / 4.0 + 10)
p3=rotate2d(60, p2, p1)



koch (p1, p2, (255,255,255))
koch (p2, p3, (255,255,255))
koch (p3, p1, (255,255,255))
sierp(p1, p2, p3, (128,255,255))

pygame.display.flip()
pygame.display.flip()

while True:
    handle_events()
    pygame.time.wait(10)
