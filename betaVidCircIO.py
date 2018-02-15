import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import style
import cv2
import RPi.GPIO as GPIO
from picamera import PiCamera, Color
from picamera.array import PiRGBArray
from time import sleep

global img_rgb
global resFactor
resFactor = 1
img_rgb = cv2.imread('/home/pi/Shared/images/image1b.jpg')
pinsGPIO = [ 6,26,20, 5,21,3,16,2,14,15]



camera = PiCamera()
camera.framerate = 32



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

def setResolution():
    resX = 1440
    resY = 900
    res = (int(resX/resFactor), int(resY/resFactor))
    return res

def drawPinRectangles():
# crop_img = img_rgb[250:600, 600:1300] #all ten
# NOTE: its img[y: y + h, x: x + w] 
    for i in range(0,10):
        a =(crop_ranges[i][2]+x,crop_ranges[i][0]+y)
        b = (crop_ranges[i][3]+x1, crop_ranges[i][1]+y1)
        a1 = (int(a[0]/resFactor), int(a[1]/resFactor))
        b1 = (int(b[0]/resFactor), int(b[1]/resFactor))
        print( a1, b1)
        cv2.rectangle(img_rgb,b1, a1, 255,2)
    cv2.imshow('BO.jpg', img_rgb) 

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

def camPicCapture(delay,x):
    # camera.start_preview()
    sleep(delay)
    # camera.capture('/home/pi/Shared/images/x1image.jpg')
    camera.annotate_text = "Brightness = "+ str(x)
    img = camera.capture_continuous('/home/pi/Shared/images/x1image.jpg')
    # camera.stop_preview()

t =[]
crop = []    
setupGPIO(pinsGPIO)
readPinImages(t)

# for x in range(0,20):
#     camPicCapture(0,x)
camera.resolution = setResolution()
rawCapture = PiRGBArray(camera, size=setResolution())
print(camera.resolution)
sleep(1)
 
# capture frames from the camera
with camera.PiCameraCircularIO(camera, splitter_port=2) as stream:
    camera.start_recording(stream, format='h264', splitter_port=2)
    for frame in camera.streams(rawCapture,format="rgb",  use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        img_rgb = frame.array
        pinCount = 0
        thisRes = (720,450)
        for i in range(0,10):
            crop.append(img_rgb[crop_ranges[i][0]+x:crop_ranges[i][1]+x1,crop_ranges[i][2]+y:crop_ranges[i][3]]+y1)
            img_gray = cv2.cvtColor(crop[i], cv2.COLOR_BGR2GRAY)
            w,h = img_gray_temp[i].shape[::-1]
            res = cv2.matchTemplate(img_gray,img_gray_temp[i],cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            threshold = 0.3
            
            if threshold > min_val:
                pinCount = pinCount + 2**(9-i)
                loc = np.where(True)
                top_left = (crop_ranges[i][2]+x+min_loc[0],crop_ranges[i][0]+y+min_loc[1])
                # bottom_right = (top_left[0] + w, top_left[1] +h)
                print(i, len(res), min_val, min_loc, pinCount)
                
                plt.scatter(top_left[1], top_left[0])
                plt.text(top_left[1], top_left[0], str(i+1)+' '+str(top_left[1])+' '+str(top_left[0])+' '+str(min_val))
        bit_GPIO(pinsGPIO,pinCount)
        # plt.show()
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            camera.stop_preview()
            break
cv2.waitKey(0)
cv2.destroyAllWindows
