import io
import random
import picamera
from PIL import Image
import cv2
import numpy

prior_image = None
global counter
counter = 0

def detect_motion(camera):
    global prior_image
    global counter
    stream = io.BytesIO()
    camera.rotation = 270
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
        # current_image = numpy.array(current_image)
        current_image = cv2.imdecode(current_image,1)
       
        cv2.imwrite('/home/pi/Shared/videos/bImg'+str(counter)+'.jpg',current_image)
        counter = counter +1
        print('TYPE', type(current_image), counter)
        # cv2.imshow('Current Image', current_image)
        # Compare current_image to prior_image to detect motion. This is
        # left as an exercise for the reader!
        result = random.randint(0, 5) == 0
        # Once motion detection is done, make the prior image the current
        prior_image = current_image
        return result

with picamera.PiCamera() as camera:
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
                stream.copy_to('/home/pi/Shared/videos/bffl'+str(counter)+'.h264', seconds=10)
                stream.clear()
                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()