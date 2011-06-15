import sys
#import and init pygame
import pygame
import random

random.seed()
pygame.init() 

#create the screen
window = pygame.display.set_mode((1200, 700)) 

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

def makeline(start, end, depth, len, color):
    color = (color[0] * ( 1 - random.random()*0.25), color[1] * ( 1 - random.random()*0.25), color[2] * ( 1 - random.random()*0.25))
    len = len + (random.random() - 0.5) * lenranfactor
    pygame.draw.line(window, color, start, mix(start, end, len))
    pygame.display.flip() 
    if depth > 0:
        makeline(mix(start, end, len), rotate2d((random.random() - 0.5) * rotranfactor  + 45 * (depth/10.0), end, mix(start, end, len)), depth -1, len, color)
        makeline(mix(start, end, len), rotate2d((random.random() - 0.5) * rotranfactor  - 45 * (depth /10.0), end, mix(start, end, len)), depth -1, len, color)
        

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

makeline((300,200), (1200,700), 10.0, 2.9/3, (255,255,255))
#draw it to the screen
#input handling (somewhat boilerplate code):
while True:
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT: 
          sys.exit(0) 
      else: 
          print event 
   pygame.time.wait(10)
