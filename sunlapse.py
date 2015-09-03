#!/usr/bin/python3

import os, datetime, time
from subprocess import Popen, PIPE
import picamera

#For easy date times.
import arrow
#For sunrise/sunset data
from astral import Astral


def start(city_name = 'Brussels', folder = 'images'):
    dawn, dusk = get_interesting_times(city_name)
    delay = get_timelapse_delay(dawn, dusk)
    time_zone_info = dawn.tzinfo

    #Get the datetime so we can make a folder for it.
    raw_time = arrow.now(time_zone_info)
    formatted_time = raw_time.format('YYYY_MM_DD-HH_mm_ss')

    #Build the folder path for datetime.
    image_folder = os.path.join(folder, formatted_time)
    if not os.path.exists(folder):
        os.makedirs(folder)

    #Initialize camera so we don't have to get a new handle every time
    camera = picamera.PiCamera()

    shot = 0
    while arrow.now(time_zone_info) < dusk:
        print('Taking picture {} at {}'.format(shot, formatted_time))
        filename = 'timelapse_{:04d}.jpeg'.format(shot)
        image_path = os.path.join(folder, filename)
        take_picture(image_path, camera)
        shot += 1
        time.sleep(delay)
    else:
        print('Finished the time lapse')


def get_interesting_times(city_name):
    #Determine sunset/sundown information
    astral = Astral()
    city = astral[city_name]
    sun = city.sun(date=datetime.date.today(), local = True)
    dawn = sun['dawn']
    dusk = sun['dusk']
    time_zone_info = dawn.tzinfo
    print('Dawn: {}'.format(dawn))
    print('Dusk: {}'.format(dusk))
    print('Now: {}'.format(datetime.datetime.now(time_zone_info)))
    return dawn, dusk


def get_timelapse_delay(dawn, dusk, total_runtime = '00:10:00', fps=24):
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


if __name__ == '__main__':
    start()