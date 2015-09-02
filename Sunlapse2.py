#!/usr/bin/python3

import os, datetime, time
from subprocess import Popen, PIPE
import picamera

#For easy datetimes.
import arrow
#For sunrise/sunset data
from astral import Astral


def start(city_name = 'Brussels', folder = 'images'):
    dawn, dusk = get_interesting_times(city_name)
    delay = get_timelapse_delay(dawn, dusk)
    tzinfo = dawn.tzinfo

    #Get the datetime so we can make a folder for it.
    raw_time = arrow.now(tzinfo)
    formatted_time = raw_time.format('YYYY_MM_DD-HH_mm_ss')

    #Build the fodler path for datetime.
    image_folder = os.path.join(folder, formatted_time)
    if not os.path.exists(folder):
        os.makedirs(folder)

    #Initialize camera so we don't have to get a new handle every time
    camera = picamera.PiCamera()

    shot = 0
    while arrow.now(tzinfo) < dusk:
        print('Taking picture {} at {}'.format(shot, formatted_time))
        filename = 'timelapse_{:04d}.jpeg'.format(shot)
        imgpath = os.path.join(folder, filename)
        take_picture(imgpath, camera)
        shot += 1
        time.sleep(delay)


def get_interesting_times(city_name):
    #Determine sunset/sundown information
    astral = Astral()
    city = astral[city_name]
    sun = city.sun(date=datetime.date.today(), local = True)
    dawn = sun['dawn']
    dusk = sun['dusk']
    tzinfo = dawn.tzinfo
    print('Dawn: {}'.format(dawn))
    print('Dusk: {}'.format(dusk))
    print('Now: {}'.format(datetime.datetime.now(tzinfo)))
    return dawn, dusk


def get_timelapse_delay(dawn, dusk, total_runtime = '00:00:06', fps=24):
    #Figure out how long we should delay between shooting frames.
    #Returns a float
    #The time from Astral are a day ahead, even though we explicitly set it.
    time_til_dusk = dusk - datetime.datetime.now(dusk.tzinfo)
    hours, minutes, seconds = total_runtime.split(':')
    print('Time until dusk: {}'.format(time_til_dusk))
    total_seconds = time_til_dusk.total_seconds()
    frame_delay = float(total_seconds) / (int(seconds) * fps)
    print('Delay: {}'.format(frame_delay))
    return frame_delay


def take_picture(filename, camera):
    #Use built-in camera.
    camera.capture(filename)

def take_gphoto_picture(filename):
    #Use gphoto2 to interact with our camera and take the picture
    process = Popen(['/usr/local/bin/gphoto2', '--capture-image-and-download', '--filename', filename], stdout= PIPE, stderr = PIPE)
    output = process.communicate()
    print('Result: {}'.format(output))

if __name__ == '__main__':
    start()