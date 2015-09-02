#!/usr/bin/env python3
from datetime import *
import picamera


def timelapse():
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        camera.start_preview()
        time.sleep(2)
        for filename in camera.capture_continuous('Timelapsel{counter:06d}.jpg'):
            print('Captured {}'.format(filename))
            time.sleep(10)


