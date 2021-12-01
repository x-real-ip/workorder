import re
import logging

## logging
logger = logging.getLogger(__name__)

def starttime(time):
    time = re.split("\D",time)
    hours = int(time[0])
    minut = int(time[1])
    if minut <= 15:
        minut = 00
    elif minut <= 30 >= 15:
        minut = 15
    elif minut <= 45 >= 30:
        minut = 30
    else:
        minut = 45
    starttime.minut = (f"{minut:02d}")
    starttime.hours = hours
    logger.info(f"using starttime: {starttime.hours}:{starttime.minut}")

def endtime(time):
    time = re.split("\D",time)
    hours = int(time[0])
    minut = int(time[1])
    if minut <= 15 >= 00:
        minut = 15
    elif minut <= 30 >= 15:
        minut = 30
    elif minut <= 45 >= 30:
        minut = 45
    else:
        minut = 00
        hours += 1
        if hours == 24:
            hours = 00
    endtime.minut = (f"{minut:02d}")
    endtime.hours = hours
    logger.info(f"using endtime: {endtime.hours}:{endtime.minut}")