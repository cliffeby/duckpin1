import io
import random
import picamera
import numpy as np
import cv2

def write_now():
    # Randomly return True (like a fake motion detection routine)
    return random.randint(0, 10) == 0

def write_video(stream):
    print('Writing video!')
    with stream.lock:
        # Find the first header frame in the video
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        # Write the rest of the stream to disk
        with io.open('/home/pi/Shared/videos/vidmon.h264', 'wb') as output:
            output.write(stream.read())

with picamera.PiCamera() as camera:
    # for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    stream = picamera.PiCameraCircularIO(camera, seconds=5)
    camera.start_recording(stream, format='h264')
    print(stream.tell())
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)
    # OpenCV returns an array with data in BGR order. If you want RGB instead
    # use the following...
    # image = image[:, :, ::-1]
    cv2.imshow("IMAAGE", image)

    try:
        while True:
            camera.wait_recording(1)
            if write_now():
                # Keep recording for 10 seconds and only then write the
                # stream to disk
                camera.wait_recording(1)
                write_video(stream)
    finally:
        camera.stop_recording()