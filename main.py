import time
import video
import cv2
from webs import *

processor = video.VideoProcessor()

neurons = {(i,j,["red","green","blue","vert","horiz"][k]):Node(1) for i in range(0,30) for j in range(0,40) for k in range(5)}

web = Web(n = neurons.values())
print(web.nodes)




result = processor.update()
if result:
    red, green, blue, edges_x, edges_y = result
    for x,i in enumerate(red):
        for y,j in enumerate(i):
            if j > 0:
                neurons[(x,y,"red")].fire(j)
    for y,i in enumerate(green):
        for x,j in enumerate(i):
            if j > 0:
                neurons[(x,y,"green")].fire(j)
    for y,i in enumerate(blue):
        for x,j in enumerate(i):
            if j > 0:
                neurons[(x,y,"blue")].fire(j)
    for y,i in enumerate(edges_x):
        for x,j in enumerate(i):
            if j > 0:
                neurons[(x,y,"vert")].fire(j)
    for y,i in enumerate(edges_y):
        for x,j in enumerate(i):
            if j > 0:
                neurons[(x,y,"horiz")].fire(j)
    


