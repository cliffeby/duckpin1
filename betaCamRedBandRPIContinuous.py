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
global current_image
global resFactor
global counter
global img_gray_temp
global crop_ranges
global priorPinCount

pinsGPIO = [ 6,26,20, 5,21,3,16,2,14,15]
lower_red = np.array([0,0,100]) # lower_red = np.array([0,100,0])
upper_red = np.array([110,110,255])  # upper_red = np.array([180,255,255])
crop_ranges = ([390,490, 820,930],[325,425, 735,835],[345,445, 960,1060],[265,365, 660,760],[280,380, 860,960],
    [300,400, 1065,1165],[260,360, 600,700],[265,365, 790,890],[270,370, 970,1070],[280,380, 1150,1250])
resFactor = 1
# img_rgb = cv2.imread('/home/pi/Shared/images/image1b.jpg')

img_gray_temp = []
current_image = []
t =[]
crop = []    
frameCount = 0
prior_image = None
counter = 0
priorPinCount = 0

#Initialze Offsets
x=15
x1=-10 +x
y=0
y1=0 + y

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
        # print(idx,bits, bits[idx])
        if(bits[idx]=="1"):
             GPIO.output(pins[idx], GPIO.HIGH)
        else:
            GPIO.output(pins[idx], GPIO.LOW)

def drawPinRectangles():
    global current_image
    # crop_img = img_rgb[250:600, 600:1300] #all ten
    # NOTE: its img[y: y + h, x: x + w] 
    for i in range(0,10):
        a =(crop_ranges[i][2]+x,crop_ranges[i][0]+y)
        b = (crop_ranges[i][3]+x1, crop_ranges[i][1]+y1)
        a1 = (int(a[0]/resFactor), int(a[1]/resFactor))
        b1 = (int(b[0]/resFactor), int(b[1]/resFactor))
        # print( a1, b1)
        cv2.rectangle(current_image, b1, a1, 255, 2)
    cv2.imshow('BO.jpg', current_image) 

def detect_motion(camera):
    global prior_image
    global priorPinCount
    global current_image
    global counter
    stream = io.BytesIO()
    camera.rotation = 270
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # current_image = np.array(current_image)
        current_image = cv2.imdecode(current_image,1)
        
        # cv2.imwrite('/home/pi/Shared/videos/bImg'+str(counter)+'.jpg',current_image)
        drawPinRectangles()

        img_rgb = current_image

        mask = cv2.inRange(img_rgb,lower_red,upper_red)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)
        output = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)
        cv2.imshow('Mask', mask)
        # cv2.imwrite('/home/pi/Shared/videos/bImgMask'+str(counter)+'.jpg', output)
        cv2.imshow('Frame',current_image)
        cv2.imshow('Output',output)
        sumHist = [0,0,0,0,0,0,0,0,0,0]

        pinCount = 0
        crop = []
        sumHist = [0,0,0,0,0,0,0,0,0,0]
       
        for i in range(0,10):
                crop.append(output[crop_ranges[i][0]+x:crop_ranges[i][1]+x1,crop_ranges[i][2]+y:crop_ranges[i][3]]+y1)
                hist = cv2.calcHist([crop[i]],[1],None,[4], [10,50])
                sumHist[i] = hist[0]+hist[1]+hist[2]+hist[3]
             
                threshold = 20
            
                if threshold < sumHist[i]:
                    pinCount = pinCount + 2**(9-i)
                
        print('HIST', counter, sumHist, pinCount)
        
                        
            #             plt.scatter(top_left[1], top_left[0])
            #             plt.text(top_left[1], top_left[0], str(i+1)+' '+str(top_left[1])+' '+str(top_left[0])+' '+str(min_val))
        bit_GPIO(pinsGPIO,pinCount)
        # plt.show()

        counter = counter +1
        if priorPinCount == pinCount:
            return False
        # prior_image = current_image
        else:
            priorPinCount = pinCount
            return True

with picamera.PiCamera() as camera:
    setupGPIO(pinsGPIO)
    camera.resolution = (1440, 900)
    # camera.rotation = 270
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
                stream.copy_to('/home/pi/Shared/videos/bffl'+str(counter)+'.h264', seconds=5)
                stream.clear()
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()
