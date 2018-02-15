import io
import math
import random
from time import sleep

import numpy as np
import picamera
import RPi.GPIO as GPIO
from matplotlib import pyplot as plt
from matplotlib import style
from picamera import Color, PiCamera
from picamera.array import PiRGBArray
from PIL import Image

import cv2

global img_rgb
global resFactor
global previousPinCount
previousPinCount = 0
resFactor = 1
img_rgb = cv2.imread('/home/pi/Shared/images/image1b.jpg')
pinsGPIO = [ 6,26,20, 5,21,3,16,2,14,15]
# camera = PiCamera()
global img_gray_temp
img_gray_temp = []
global crop_ranges
crop_ranges = ([390,610, 820,930],[325,535, 735,835],[345,560, 960,1060],[265,475, 660,760],[280,500, 860,960],
    [300,510, 1065,1165],[260,450, 600,700],[265,455, 790,890],[270,460, 970,1070],[280,490, 1150,1250])

#Initialze Offsets
x=10
x1=0 +x
y=0
y1=0 + y

prior_image = None
global counter
counter = 0
crop =[]

def readPinImages(t):
    t.append(cv2.imread('/home/pi/Shared/images/pinOne.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinTwo.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinThree.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinFour.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinFive.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinSix.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinSeven.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinEight.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinNineA.jpg'))
    t.append(cv2.imread('/home/pi/Shared/images/pinTen.jpg'))
    
    for index,template in enumerate(t):
        img_gray_temp.append(cv2.cvtColor(t[index], cv2.COLOR_BGR2GRAY))
        print(len(img_gray_temp))

def setupGPIO(pins):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in pins:
        GPIO.setup(pin,GPIO.OUT)
        print ("setup Completed")

def bit_GPIO(pins,pinCount):
    bits = "{0:b}".format(pinCount)
    while len(bits)<10:
        bits = "0"+bits
    for idx in range(0,len(bits)):
        print(idx,bits, bits[idx])
        if(bits[idx]=="1"):
             GPIO.output(pins[idx], GPIO.HIGH)
        else:
            GPIO.output(pins[idx], GPIO.LOW)

def detect_motion(camera):
    global prior_image
    global counter
    global previousPinCount
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = Image.open(stream).convert('RGB')
        img_rgb = np.array(current_image)

        pinCount = 0
    
        for i in range(0,10):
            crop.append(img_rgb[crop_ranges[i][0]+x:crop_ranges[i][1]+x1,crop_ranges[i][2]+y:crop_ranges[i][3]]+y1)
            img_gray = cv2.cvtColor(crop[i], cv2.COLOR_BGR2GRAY)
            w,h = img_gray_temp[i].shape[::-1]
            res = cv2.matchTemplate(img_gray,img_gray_temp[i],cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            threshold = 0.6
            
            if threshold > min_val:
                pinCount = pinCount + 2**(9-i)
                loc = np.where(True)
                top_left = (crop_ranges[i][2]+x+min_loc[0],crop_ranges[i][0]+y+min_loc[1])
                # bottom_right = (top_left[0] + w, top_left[1] +h)
                print(i, len(res), min_val, min_loc, pinCount)
                
                plt.scatter(top_left[1], top_left[0])
                plt.text(top_left[1], top_left[0], str(i+1)+' '+str(top_left[1])+' '+str(top_left[0])+' '+str(min_val))
        if previousPinCount != pinCount:
            previousPinCount = pinCount
            bit_GPIO(pinsGPIO,pinCount)

            cv2.imwrite('/home/pi/Shared/videos/beforeImg'+str(counter)+'.jpg',img_rgb)
            print('TYPE', type(img_rgb))
            counter = counter +1
            cv2.imshow('Current Image', img_rgb)
            # Compare current_image to prior_image to detect motion. This is
            # left as an exercise for the reader!

            # result = random.randint(0, 10) == 0
            # # Once motion detection is done, make the prior image the current
            # prior_image = current_image
            return True
        else:
            return False

t =[]
crop = []    
setupGPIO(pinsGPIO)
readPinImages(t)


with PiCamera() as camera:
    camera.resolution = (1440, 900)
    camera.rotation = 270
    stream = picamera.PiCameraCircularIO(camera, seconds=5)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            if detect_motion(camera):
                print('Motion detected!')
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording('after.h264')
                # Write the 10 seconds "before" motion to disk as well
                stream.copy_to('/home/pi/Shared/videos/before'+str(counter)+'.h264', seconds=10)
                stream.clear()
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()
