from picamera import PiCamera, Color
from time import sleep
import datetime as dt
import time

camera = PiCamera()

camera.start_preview()
sleep(1)
camera.stop_preview()

def camRotation(degrees):
    camera.start_preview
    camera.rotation = 90
    camera.start_preview()
    sleep(1)
    camera.stop_preview()

def camBrightness():
    camera.start_preview()
    camera.annotate_background = Color('blue')
    camera.annotate_foreground = Color('yellow')
    for i in range(100):
        camera.brightness = i
        camera.annotate_text = "B-"+ str(i)
        sleep(0.25)
        camera.capture('/home/pi/Shared/images/bright.jpg')
    camera.stop_preview()
    camera.brightness = 50
    camera.annotate_background = Color('blue')
    camera.annotate_foreground = Color('yellow')

def camPicCapture(numberOfPics, delay):
    camera.start_preview()
    camera.annotate_background = Color('blue')
    camera.annotate_foreground = Color('yellow')
    camera.annotate_text = " Hello duckpin world "+ dt.datetime.now().isoformat('0')
    for i in range(numberOfPics):
        sleep(delay)
        camera.annotate_text = " Hello duckpin1 world "+ dt.datetime.now().isoformat('0')
        camera.capture('/home/pi/Shared/images/image%s.jpg' % i)
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
        camera.annotate_text = " Hello duckpin1 world "+ dt.datetime.now().isoformat('0')
        camera.start_recording('/home/pi/Shared/videos/video%s.h264' % i)
        sleep(videoLength)
        camera.stop_recording()
    camera.stop_preview()
    camera.annotate_text = ""
    camera.annotate_background
    camera.annotate_foreground

camRotation(90)
camPicCapture(5,1)
camVideoCapture(3,3,1)

