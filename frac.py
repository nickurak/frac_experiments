#!/usr/bin/env python
import sys
import pygame
import random

random.seed()
pygame.init() 

frameskip = 5000
#create the screen
window = pygame.display.set_mode((1920, 1200)) 

#draw a line - see http://www.pygame.org/docs/ref/draw.html for more 
#pygame.draw.line(window, (255, 255, 255), (0, 0), (30, 50))

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
maxdepth=5

def makeline(start, end, depth, len, color):
    color = (color[0] * ( 1 - random.random()*0.25), color[1] * ( 1 - random.random()*0.25), color[2] * ( 1 - random.random()*0.25))
    len = len + (random.random() - 0.5) * lenranfactor
    len = (len+ 1-(1-len) * (depth/maxdepth*2.0))/2
    pygame.draw.line(window, color, start, mix(start, end, len))
    pygame.display.flip() 
    if depth > 0:
        makeline(mix(start, end, len), rotate2d((random.random() - 0.5) * rotranfactor  + 30, end, mix(start, end, len)), depth -1, len, color)
        makeline(mix(start, end, len), rotate2d((random.random() - 0.5) * rotranfactor  - 30, end, mix(start, end, len)), depth -1, len, color)
        

#        makeline(mix(start, end, len), rotate2d(30, end, mix(start, end, len)), depth -1)
#        makeline(mix(start, end, len), rotate2d(-30, end, mix(start, end, len)), depth -1)
#        makeline(mix(start, end, 0.5/3), rotate2d(30, end, mix(start, end, 0.5/3)), depth -1)
#        makeline(mix(start, end, 0.5/3), rotate2d(-30, end, mix(start, end, 0.5/3)), depth -1)
#    pygame.draw.line(window, color, mix(start, end, 0.5/3), end)
#    pygame.display.flip() 
    for event in pygame.event.get(): 
       if event.type == pygame.QUIT: 
           sys.exit(0) 
       else: 
           print event 

i = 0

def sierp(a, b, c, color, depth):
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
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit(0) 
            else: 
                print event 
    if (depth > 0):
        color2 = (color[0] * 0.5, color[1] * 0.25, color[2] * 0.25)
        sierp(p1, p2, p3, color2, depth - 1)
        color2 = (color[0] * 0.5, color[1], color[2])
        sierp(a, p1, p3, color2, depth - 1)
        color2 = (color[0], color[1] * 0.5, color[2])
        sierp(p1, b, p2, color2, depth - 1)
        color2 = (color[0], color[1], color[2] * 0.5)
        sierp(p3, p2, c, color2,depth - 1)

def koch(start, end, depth, color):
    global i
    depth = depth - 1
#    if color[1] > 32:
#        color = (color[0] * ( 1 - random.random()*0.1), color[1] * ( 1 - random.random()*0.1), color[2])
#    else:
#        color = (color[0] * ( 1 - random.random()*0.1), color[1], color[2] * ( 1 - random.random()*0.1))
#    p1 = mix(start, end, (2.25-random.random()*0.5)/3)
#    p3 = mix(start, end, (1.25-random.random()*0.5)/3)
#    p2 = rotate2d(-60+random.random()*60-30, p3, p1)
    p1 = mix(start, end, 2.0/3)
    p3 = mix(start, end, 1.0/3) 
#    p2 = rotate2d(-60, p3, p1)
    p2 = rotate2d(-60, p3, p1)
    if depth > 0:
        color2 = (color[0], color[1] * 0.5, color[2])
        color = (color[0], color[1], color[2] * 0.5)
        koch(start, p1, depth, color)
        koch(p1, p2, depth, color2)
        koch(p2, p3, depth, color2)
        sierp(p1, p2, p3, color2, depth)
#        koch(p2, p1, depth, color2)
#        koch(p3, p2, depth, color2)
        koch(p3, end, depth, color)
    else:
        pygame.draw.line(window, color, start, end)
        i = i + 1
        if (i == frameskip):
            pygame.display.flip() 
            i = 0
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    sys.exit(0) 
                else: 
                    print event 

p1=(0,300)
p2=(1039,300)
p3=rotate2d(60, p2, p1)

maxdepth=9
koch (p1, p2, maxdepth, (128,255,255))
koch (p2, p3, maxdepth, (128,255,255))
koch (p3, p1, maxdepth, (128,255,255))
sierp(p1, p2, p3, (128,255,255), maxdepth)
pygame.display.flip() 


maxdepth = 10
p1=(225,25)
p2=(975,25)
p3=rotate2d(60, p2, p1)

#pygame.draw.line(window, (255,255,255), p1, p2)
#pygame.draw.line(window, (255,255,255), p2, p3)
#pygame.draw.line(window, (255,255,255), p3, p1)
#sierp(p1, p2, p3, (255, 255, 255), maxdepth)
pygame.display.flip() 

print "done"
#makeline((600, 150), (600,800), maxdepth, 2.9/3, (255,255,255))
#draw it to the screen
#input handling (somewhat boilerplate code):
while True:
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT: 
          sys.exit(0) 
      else: 
          print event 
   pygame.time.wait(10)
