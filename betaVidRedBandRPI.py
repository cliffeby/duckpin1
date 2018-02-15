import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import style
import cv2
import RPi.GPIO as GPIO
# from picamera import PiCamera, Color
# from picamera.array import PiRGBArray
from time import sleep

global img_rgb
global resFactor
resFactor = 1
img_rgb = cv2.imread('/home/pi/Shared/images/image1b.jpg')
pinsGPIO = [ 6,26,20, 5,21,3,16,2,14,15]



# camera = PiCamera()
# camera.framerate = 32



global img_gray_temp
img_gray_temp = []
global crop_ranges
crop_ranges = ([390,490, 820,930],[325,425, 735,835],[345,445, 960,1060],[265,365, 660,760],[280,380, 860,960],
    [300,400, 1065,1165],[260,360, 600,700],[265,365, 790,890],[270,370, 970,1070],[280,380, 1150,1250])

#Initialze Offsets
x=15
x1=-10 +x
y=0
y1=0 + y



def drawPinRectangles():
# crop_img = img_rgb[250:600, 600:1300] #all ten
# NOTE: its img[y: y + h, x: x + w] 
    for i in range(0,10):
        a =(crop_ranges[i][2]+x,crop_ranges[i][0]+y)
        b = (crop_ranges[i][3]+x1, crop_ranges[i][1]+y1)
        a1 = (int(a[0]/resFactor), int(a[1]/resFactor))
        b1 = (int(b[0]/resFactor), int(b[1]/resFactor))
        # print( a1, b1)
        cv2.rectangle(img_rgb,b1, a1, 255,2)
    cv2.imshow('BO.jpg', img_rgb) 

def readPinImages(t):
    t.append(cv2.imread('/home/pi/Shared/images/redBand.jpg'))
    # t.append(cv2.imread('P:/images/redBand.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinTwo.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinThree.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinFour.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinFive.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinSix.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinSeven.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinEight.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinNineA.jpg'))
    # t.append(cv2.imread('/home/pi/Shared/images/pinTen.jpg'))
    
    for index,template in enumerate(t):
        img_gray_temp.append(cv2.cvtColor(t[index], cv2.COLOR_BGR2GRAY))
        print(len(img_gray_temp))

def setupGPIO(pins):
    # print('Fake Setup')
    # return
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in pins:
        GPIO.setup(pin,GPIO.OUT)
        print ("setup Completed")

def bit_GPIO(pins,pinCount):
    # print('Fake PinCount', pinCount)
    # return
    bits = "{0:b}".format(pinCount)
    while len(bits)<10:
        bits = "0"+bits
    for idx in range(0,len(bits)):
        # print(idx,bits, bits[idx])
        if(bits[idx]=="1"):
             GPIO.output(pins[idx], GPIO.HIGH)
        else:
            GPIO.output(pins[idx], GPIO.LOW)



t =[]
crop = []    
setupGPIO(pinsGPIO)
# readPinImages(t)
frameCount = 0
lower_red = np.array([0,0,100])
upper_red = np.array([110,110,255])
    # lower_red = np.array([0,100,0])
    # upper_red = np.array([180,255,255])

# for x in range(0,20):
#     camPicCapture(0,x)
# camera.resolution = setResolution()
# rawCapture = PiRGBArray(camera, size=setResolution())
# print(camera.resolution)
# sleep(1)
rawCapture = '/home/pi/Shared/videos/video3d.h264'
cap = cv2.VideoCapture(rawCapture)
color = ('b', 'g', 'r')
while(cap.isOpened()):
# capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    # img_rgb = []
    crop = []
    ret, frame = cap.read()
    frameCount = frameCount+1
    img_rgb = frame
    drawPinRectangles()
    pinCount = 0
    
    mask = cv2.inRange(img_rgb,lower_red,upper_red)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)
    output = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)
    # cv2.imshow('Mask', mask)
    # cv2.imshow('Frame',frame)
    cv2.imshow('Output',output)
    sumHist = [0,0,0,0,0,0,0,0,0,0]
    # if frameCount>10:
    #     frame1 = frame
    #     cv2.imshow('DownPins', frame1)
    # cv2.imwrite( 'P:/videos/OUTPUT.jpg', output)
    
    for i in range(0,10):
                crop.append(output[crop_ranges[i][0]+x:crop_ranges[i][1]+x1,crop_ranges[i][2]+y:crop_ranges[i][3]]+y1)
                hist = cv2.calcHist([crop[i]],[1],None,[4], [10,50])
                sumHist[i] = hist[0]+hist[1]+hist[2]+hist[3]
        
            # for i,col in enumerate(color):
            #     plt.plot(hist,color = col)
            #     plt.xlim([0,256])
            # plt.show()
    
                threshold = 20
            
                if threshold < sumHist[i]:
                    pinCount = pinCount + 2**(9-i)
                    # loc = np.where(True)
                    # top_left = (crop_ranges[i][2]+x+min_loc[0],crop_ranges[i][0]+y+min_loc[1])
                    #     # bottom_right = (top_left[0] + w, top_left[1] +h)
                    # print(i, len(res), min_val, min_loc, pinCount)
    print('HIST',frameCount, sumHist, pinCount)
                
    #             plt.scatter(top_left[1], top_left[0])
    #             plt.text(top_left[1], top_left[0], str(i+1)+' '+str(top_left[1])+' '+str(top_left[0])+' '+str(min_val))
    bit_GPIO(pinsGPIO,pinCount)
    # plt.show()
    
    key = cv2.waitKey(1) & 0xFF
    # rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        camera.stop_preview()
        break

cv2.waitKey(0)
cv2.destroyAllWindows
