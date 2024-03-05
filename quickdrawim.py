from quickdraw import QuickDrawDataGroup
#from PIL import Image, ImageDraw
import cv2
import numpy as np
import time
import sys

def quickdoodle(doodle, exit_event):
    #cv2.namedWindow("Canvas")
    while True:
        if exit_event.is_set():
            print("kill quickdraw")
            sys.exit()
        if not doodle.empty():
            print("getting doodle")
            dood = str(doodle.get())
            cv2.namedWindow(dood)
            cv2.moveWindow(dood, 800, 300)
            qd = QuickDrawDataGroup(dood, max_drawings=100, recognized=True)
            for i, draw in enumerate(qd.drawings):
                if exit_event.is_set():
                    print("kill quickdraw")
                    sys.exit()
                if not doodle.empty():
                        break
                draw_img = np.ones((255, 255, 3), np.uint8)*255
                for stroke in draw.strokes:
                    for coordinate in range(len(stroke)-1):
                        x1 = stroke[coordinate][0]
                        #print(f'x1{x1}')
                        y1 = stroke[coordinate][1]
                        x2 = stroke[coordinate+1][0]
                        #print(f'x2{x2}')
                        y2 = stroke[coordinate+1][1]
                        cv2.line(draw_img, (x1, y1), (x2, y2), (0, 0, 0), 4)
                        cv2.imshow(dood, draw_img)
                        cv2.waitKey(1)
                        time.sleep(0.1)
                time.sleep(4)
        time.sleep(0.1)
        pass