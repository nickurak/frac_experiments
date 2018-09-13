#!/usr/bin/env python
import sys
import pygame
import random

random.seed()
pygame.init() 


frameskip = 5000
#create the screen
window = pygame.display.set_mode((1920, 1080))

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


i = 0

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
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit(0) 
            else: 
                print event
    mindif = 12
    if abs(p1[0] - p3[0]) + abs(p1[0] - p2[0]) + abs(p2[0] - p3[0]) > mindif or abs(p1[1] - p3[1]) + abs(p1[1] - p2[1]) + abs(p2[1] - p3[1]) > mindif:
        color2 = (color[0] * 0.5, color[1] * 0.25, color[2] * 0.25)
        sierp(p1, p2, p3, color2)
        color2 = (color[0] * 0.5, color[1], color[2])
        sierp(a, p1, p3, color2)
        color2 = (color[0], color[1] * 0.5, color[2])
        sierp(p1, b, p2, color2)
        color2 = (color[0], color[1], color[2] * 0.5)
        sierp(p3, p2, c, color2)

def koch(start, end, color):
    global i
    p1 = mix(start, end, 2.0/3)
    p3 = mix(start, end, 1.0/3) 
    p2 = rotate2d(-60, p3, p1)
    mindif = 2
    if abs(p1[0] - p3[0]) + abs(p1[0] - p2[0]) + abs(p2[0] - p3[0]) > mindif or abs(p1[1] - p3[1]) + abs(p1[1] - p2[1]) + abs(p2[1] - p3[1]) > mindif:
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
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    sys.exit(0) 
                else: 
                    print event 

p1=(0,250)
p2=(800,250)
p3=rotate2d(60, p2, p1)

koch (p1, p2, (128,255,255))
koch (p2, p3, (128,255,255))
koch (p3, p1, (128,255,255))
sierp(p1, p2, p3, (128,255,255))
pygame.display.flip() 


pygame.display.flip() 

print "done"
#draw it to the screen
#input handling (somewhat boilerplate code):
while True:
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT: 
          sys.exit(0) 
      else: 
          print event 
   pygame.time.wait(10)
