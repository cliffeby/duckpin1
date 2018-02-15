from picamera import PiCamera, Color
import datetime as dt
import time
from time import sleep

camera = PiCamera()
# camera.resolution = (1440,1220)

def camPreview(howLong):
    camera.start_preview()
    sleep(howLong)
    camera.stop_preview()

def camRotation(degrees):
    camera.start_preview
    camera.rotation = 90
    camera.start_preview()
    sleep(1)
    camera.stop_preview()
    camera.rotation = 180
    camera.start_preview()
    sleep(1)
    camera.stop_preview()
    camera.rotation = 270
    camera.start_preview()
    sleep(1)
    camera.stop_preview()

def camBrightness():
    camera.start_preview()
    camera.annotate_background = Color('blue')
    camera.annotate_foreground = Color('yellow')
    for i in range(100):
        camera.brightness = i
        camera.annotate_text = "Brightness = "+ str(i)
        sleep(0.15)
    camera.stop_preview()
    camera.brightness = 45
    camera.annotate_background 
    camera.annotate_foreground 

def camContrast():
    camera.start_preview()
    camera.annotate_background = Color('blue')
    camera.annotate_foreground = Color('yellow')
    for i in range(-100,100):
        camera.contrast = i
        camera.annotate_text = "Contrast = "+ str(i)
        sleep(0.15)
    camera.stop_preview()
    camera.contrast = 20
    camera.annotate_background 
    camera.annotate_foreground 

def camPicCapture(numberOfPics, delay):
    camera.start_preview()
    camera.annotate_background = Color('blue')
    camera.annotate_foreground = Color('yellow')
    camera.annotate_text = " Hello duckpin world "+ dt.datetime.now().isoformat('0')
    for i in range(numberOfPics):
        sleep(delay)
        camera.annotate_text = " Hello duckpin1 world pic "+ dt.datetime.now().isoformat('0')
        camera.capture('/home/pi/Shared/images/aimage%s.jpg' % i)
    camera.stop_preview()
    camera.annotate_text = ""
    camera.annotate_background
    camera.annotate_foreground

def camVideoCapture(numberOfVideos, videoLength, delayBetweenVideos):
    camera.start_preview()
    camera.annotate_background = Color('blue')
    camera.annotate_foreground = Color('yellow')
    for i in range(numberOfVideos):
        sleep(delayBetweenVideos)
        camera.annotate_text = " Hello duckpin1 world video "+ dt.datetime.now().isoformat('0')
        camera.start_recording('/home/pi/Shared/videos/avideo%s.h264' % i)
        sleep(videoLength)
        camera.stop_recording()
    camera.stop_preview()
    camera.annotate_text = ""
    camera.annotate_background
    camera.annotate_foreground

camera.vflip = True
camera.hflip = True
camRotation(0)
camPreview(10)
camBrightness()
camContrast()
camPicCapture(3,1)
camVideoCapture(7,15,1)

