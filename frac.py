#!/usr/bin/env python
import sys
import pygame
import random

random.seed()
pygame.init() 


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

def maxsep(p1, p2, p3):
    m = 0
    m = max(m, abs(p1[0] - p2[0]))
    m = max(m, abs(p2[0] - p3[0]))
    m = max(m, abs(p3[0] - p1[0]))
    m = max(m, abs(p1[1] - p2[1]))
    m = max(m, abs(p2[1] - p3[1]))
    m = max(m, abs(p3[1] - p1[1]))
    return m


ip1=(10, fh / 4.0 + 10)
ip2=(w+10, fh / 4.0 + 10)
ip3=rotate2d(60, ip2, ip1)

initsep=maxsep(ip1, ip2, ip3)

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
    return (a[0] / r + b[0] * (r-1) / r, a[1] / r + b[1] * (r-1) / r)



lenranfactor=0.005
rotranfactor=10
lenranfactor=0.0
rotranfactor=0


i = 0

sierpstack=[]

def sierp(a, b, c, color):
    global i
    p1=mix(a, b, 2)
    p2=mix(b, c, 2)
    p3=mix(c, a, 2)

    pygame.draw.line(window, color, p1, p2)
    pygame.draw.line(window, color, p2, p3)
    pygame.draw.line(window, color, p3, p1)
    i = i + 1
    if (i == frameskip):
        pygame.display.flip() 
        i = 0
        handle_events()
    sep = maxsep(p1, p2, p3)
    if sep > 6:
        color2 = (255 * float(sep)/initsep, 255 * float(sep)/initsep, 255 * float(sep) / initsep)
        sierpstack.append((p1, p2, p3, color2))
        color3 = (color[0] * 0.7, color[1], color[2])
        sierpstack.append((a, p1, p3, color3))
        color3 = (color[0], color[1] * 0.7, color[2])
        sierpstack.append((p1, b, p2, color3))
        color3 = (color[0], color[1], color[2] * 0.7)
        sierpstack.append((p3, p2, c, color3))

def koch(start, end, color):
    global i
    p1 = mix(end, start, 3)
    p3 = mix(start, end, 3)
    p2 = rotate2d(-60, p3, p1)
    sep = maxsep(p1, p2, p3)
    if sep > 1:
        color2 = (color[0], color[1] * 0.5, color[2])
        color = (color[0], color[1], color[2] * 0.5)
        koch(start, p1, color)
        koch(p1, p2, color2)
        koch(p2, p3, color2)
        koch(p3, end, color)
    if sep > 6:
        sierpstack.append((p1, p2, p3, color2))
    else:
        pygame.draw.line(window, color, start, end)
        i = i + 1
        if (i == frameskip):
            pygame.display.flip() 
            i = 0
            handle_events()



koch (ip1, ip2, (255,255,255))
koch (ip2, ip3, (255,255,255))
koch (ip3, ip1, (255,255,255))
sierp(ip1, ip2, ip3, (128,255,255))

print len(sierpstack)
while len(sierpstack) > 0:
    params = sierpstack.pop(0)
    sierp(params[0], params[1], params[2], params[3])

pygame.display.flip()
pygame.display.flip()

while True:
    handle_events()
    pygame.time.wait(10)
