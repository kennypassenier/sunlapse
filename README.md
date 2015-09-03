This script is for use with a Raspberry Pi and the official Raspberry Pi Camera Module.
Once you run this, it should ask you how many days you want to capture.
It will then ask you how long you want your movie file to be.
The capture will begin with the data provided.

Example: 
- You want to make a time lapse video that lasts 1 minute over the span of 4 days.
- So the script will take the equivalent of 15 seconds every day (15 seconds * 24 fps =  360 pictures)
- If dawn is at 6am and dusk is at 6pm, it will take a picture every 2 minutes (30 pictures per hour * 12 hours = 360 pictures)

After this is all said and done, the script will convert all those pictures into one .mp4 movie file..