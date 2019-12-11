#!/usr/bin/env python3

import numpy as np
import cv2
import sys
from ledcontroller import LEDController
from ledfinder import LEDFinder
import time


def calibrate(numleds, videodevnumber=0, minpixels=20):
    # Cretate dict with mapping id -> pixelpos
    mapping_dict = {}

    # create video capture
    cap = cv2.VideoCapture(videodevnumber)

    ledc = LEDController(numleds)
    ledf = LEDFinder(minpixels)

    for i in range(numleds):
        # turn led on
        ledc.set_single_led(i)
        time.sleep(1)

        img = None

        # grab image (repeat 5x because there seems to be a buffer in some webcams)
        for _ in range(5):
            _, img = cap.read()
            cv2.imwrite(str(i)+".png", img)

        # find ledposition
        coords = ledf.find_led_coords(img)
        time.sleep(2)

        ledc.all_off()
        time.sleep(2)
        
        # add ledpos to dict if it was found
        if(coords):
            mapping_dict[i] = coords

    cap.release()
    cv2.destroyAllWindows()

def calibrate_from_files(numleds, data_folder, minpixels=20):
    mapping_dict = {}

    ledf = LEDFinder(minpixels)

    for i in range(numleds):
        # load image
        img = cv2.imread(data_folder + str(i) + ".png")

        # find ledposition
        coords = ledf.find_led_coords(img)
        dbgimg = cv2.circle(img, coords, 3, (0,0,255), 2)
        cv2.imshow('dbg', dbgimg)
        cv2.waitKey(0)

        if coords:
            mapping_dict[i] = coords
    return mapping_dict

def export_mapping(path, mapping):
    np.savetxt(path, np.array([[i,x,y] for (i,(x,y)) in mapping.items()], dtype=int))

if __name__ == '__main__':
    numleds = None
    export_path = None
    data_folder = None
    if len(sys.argv) == 3:
        numleds = int(sys.argv[1])
        export_path = sys.argv[2]
        mapping_dict = calibrate(numleds, 2)
        export_mapping(export_path, mapping_dict)

    elif len(sys.argv) == 4:
        numleds = int(sys.argv[1])
        data_folder = sys.argv[2] if sys.argv[2].endswith('/') else (sys.argv[2]+'/')
        export_path = sys.argv[3]
        mapping_dict = calibrate_from_files(numleds, data_folder)
        export_mapping(export_path, mapping_dict)
    else:
        print('Wrong number of arguments!')
        print('Usage: python treecalib.py <# LEDs> <export_path> '
                '|| python treecalib.py <# LEDs> <data_folder> <export_path>')
        sys.exit(-1)

    
