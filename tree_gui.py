#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
from ledcontroller import LEDController
import time

drawing = False
ix, iy = -1, -1
calib = None
contours = None
radius = 25
#ledc = LEDController(30)

color = (0,0,0)

def plot_tree_config(turn_90_deg=False, res=(640,480)):
    global calib, contours

    # plot LED positions
    for row in calib:
        gui = cv2.circle(img, (row[1],row[2]), 5, (128,128,128), 2)

    # draw tree contours
    for (x1,y1,x2,y2) in contours:
        gui = cv2.line(img, (x1,y1), (x2,y2), (100, 140, 0), 2)

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img, (x,y), radius, color, -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img, (x,y), radius, color, -1)
    plot_tree_config()

def get_config():
    global calib, ledc, conf
    conf = np.zeros((30,3), np.uint8)
    for row in calib:
        conf[row[0]] = img[row[2],row[1]][::-1]
    
    #ledc.set_config(conf)
    time.sleep(0.1)

def convert_calib(calib):
    calib_ = np.zeros(calib.shape, int)
    for i in range(calib.shape[0]):
        calib_[i,0] = calib[i,0]
        calib_[i,1] = calib[i,2]
        calib_[i,2] = 640 - calib[i,1]
    return calib_

def convert_contours(contours):
    contours_ = np.zeros(contours.shape, int)
    for i in range(contours.shape[0]):
        contours_[i,0] = contours[i,1]
        contours_[i,1] = 640-contours[i,0]
        contours_[i,2] = contours[i,3]
        contours_[i,3] = 640-contours[i,2]
    return contours_

if __name__ == '__main__':
    if len(sys.argv) == 3:
        calib = np.loadtxt(sys.argv[1])
        contours = np.loadtxt(sys.argv[2])
        calib = convert_calib(calib.astype(int))
        contours = convert_contours(contours.astype(int))

        img = np.zeros((640,480, 3), np.uint8)
        plot_tree_config()
        cv2.namedWindow('gui')
        cv2.setMouseCallback('gui', draw_circle)

        while(1):
            cv2.imshow('gui', img)
            get_config()
            k = cv2.waitKey(1) & 0xFF
            if k == ord('k'):
                color = (0,0,0)
            if k == ord('r'):
                color = (0, 0, 254)
            if k == ord('b'):
                color = (254,0,0)
            if k == ord('g'):
                color = (0,254,0)
            if k == ord('w'):
                color = (254, 254, 254)
            if k == ord('c'):
                color = (254, 254, 0)
            if k == ord('m'):
                color = (254, 0, 254)
            if k == ord('y'):
                color = (0, 254, 254)
            if k == 13:
                img = np.zeros((640, 480, 3), np.uint8)
                plot_tree_config()
            if k == 43:
                radius += 5
            if k == 45:
                if k > 10:
                    radius -= 5
            if k == 27:
                break
        cv2.destroyAllWindows()
    else:
        print("Usage: python tree_gui.py <calib_file_path> <tree_contours>")
