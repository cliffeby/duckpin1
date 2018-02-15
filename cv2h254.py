# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
 
# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.rotation = 270
# camera.resolution = (640,480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(camera.resolution))
 
# # allow the camera to warmup
# time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	lower_red = np.array([50,30,100])
	upper_red = np.array([255,255,255])
	mask = cv2.inRange(hsv, lower_red, upper_red)
	res = cv2.bitwise_and(image,image, mask = mask)
	
	cv2.imshow('frame', image)
	cv2.imshow('mask', mask)
	cv2.imshow('res', res)
 
	# show the frame
	# cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break