"""we checken rond 1AM voor de sunset/sundown data, dan zetten we die parameters in het script, sunset begint script tot sundown, start again"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import *
import time
#import picamera                                          #later activeren!!!!!

"""
misschien moet ik Projectdata hier leegmaken zodat ik elke keer een text bestand heb met alleen de data van het laatste project, bij elke iteratie van scrapedata() kan ik dan nog altijd appenden

"""
#We need to declare these so we can use them later in our scrapedata() function
sunrise = ""
sunset = ""

def dynamicurl():
    """returns the daily url that we need for scraping purposes"""
    #Function is automatically used in scrapedata()
    staticurl = 'http://www.sunrise-and-sunset.com/en/belgium/kampenhout/'
    datum = datetime.now()
    fmt = "%Y/%B/%d"
    now = datum.strftime(fmt)
    return staticurl+now

def scrapedata():
    """sets the sunrise and sunset variables to the correct times for that day"""
    #Initialise globals
    global sunrise
    global sunset
    #Initialise empty temporary variables to append to
    risetemp2 = ""
    settemp2 = ""
    #BeautifulSoup magic
    url = dynamicurl()
    content = urlopen(url).read()
    soup = BeautifulSoup(content)
    #Find the first table in the html, which is the one we need to scrape
    tableSoup = soup.find('table')
    #Open a file and write the table into the text file
    file = open("sundata.txt", 'w')
    file.write(str(tableSoup))
    file.close()
    #After we closed the file, open it again, this time for reading
    file2 = open('sundata.txt', 'r')
    #Use this so we can use the [:] to specify specific lines in the document
    lines = file2.readlines()
    #Declare temporary variables for sundown and sunset according to their specific position in the document (sunrise is at line 16, sunset at 24)
    risetemp = lines[16]
    settemp = lines[24]
    file2.close()
    #Iterate over the resulting temp variables to get rid of the <td> tags
    for i in risetemp:
        if not i in '</td>':
            risetemp2 += i
    for j in settemp:
        if not j in '</td>':
            settemp2 += j
    #Clean up the second temp variables so it ONLY contains the data we want
    sunrise = risetemp2[0:5]
    sunset = settemp2[0:5]
    #Now append this data to a text file with info about everyday the program ran
    projectfile = open('Projectdata.txt', 'a')
    projectfile.write('Today is %s\nSunrise: %s\nSundown: %s\n\n' % (datetime.today(), sunrise, sunset))
    projectfile.close()


def timelapse():
    print('Zogezegd doen we nu dienen timelapse')
    time.sleep(30)
    """
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 1024)
        camera.start_preview()
        time.sleep(2)
        for filename in camera.capture_continuous('sunlapse{counter:06d}.jpg'):
            print('Captured %d' % (filename))
            time.sleep(60) #Wait x seconds
"""
"""
from fractions import Fraction

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 1024)
    # Set a framerate of 1/6fps, then set shutter
    # speed to 6s and ISO to 800
    camera.framerate = Fraction(1, 6)
    camera.shutter_speed = 6000000
    camera.exposure_mode = 'off'
    camera.ISO = 800
    # Give the camera a good long time to measure auto white balance
    # (you may wish to use fixed AWB instead)
    sleep(10)
    # Finally, capture an image with a 6s exposure. Due
    # to mode switching on the still port, this will take
    # longer than 6 seconds
    camera.capture('dark.jpg')
"""


def sunisshining():
    global sunrise
    global sunset
    todaysunrise = datetime.strptime(sunrise, '%H:%M').replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    todaysunset = datetime.strptime(sunset, '%H:%M').replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)


    if todaysunrise <= datetime.now() and todaysunset >= datetime.now():
        return True
    else:
        return False

#------------------------------------- Start of actual code ------------------------------------------

scrapedata()
#Infinite loop zodat we altijd blijven draaien
while 1:
    #Als het in dit geval 1 am is dan scrapen we
    while time.strftime("%H") == "1" and time.strftime("%M") == "00":
        scrapedata()
    #Als het niet meer 1 am is dan beginnen we terug te lapsen (met nieuwe scrape data)
    else:
        #Maar alleen als er zonlicht is
        while sunisshining():
            timelapse()
