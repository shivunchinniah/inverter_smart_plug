import tinytuya

import os
from dotenv import load_dotenv
import httpx
import csv
from datetime import date, datetime, timedelta, time
from dateutil import parser
import bisect
import pytz

load_dotenv()  # take environment variables from .env.

load_shedding_url = "https://github.com/beyarkay/eskom-calendar/releases/download/latest/machine_friendly.csv"


area = os.getenv("LOAD_SHEDDING_AREA")


def load_shedding_next_mins(now=datetime.now()):
    # Pull from load shedding calendar
    schedule = []
    starts = []
    ends = []
    stages = []

    with httpx.stream("GET", load_shedding_url, follow_redirects=True) as r:
        for row in csv.reader(r.iter_lines()):
            if row[0] == area:
                schedule.append(row)
                starts.append(parser.parse(row[1]))
                ends.append(parser.parse(row[2]))
                stages.append(row[3])
    starts.sort()
    ends.sort()

    now = now.replace(tzinfo=pytz.timezone(os.getenv('TIMEZONE')))
    #now = datetime.now(tz=pytz.timezone(os.getenv('TIMEZONE'))) 
    index = bisect.bisect_left(ends, now) 

    if (index >= len(starts)):
        raise Exception("No load shedding scheduled.")

    start_mins = (starts[index]-now).total_seconds() / 60
    end_mins = (ends[index]-now).total_seconds() / 60

    return start_mins, end_mins, stages[index]

def write_error(message):
    write_log_file(message, 'error.txt')

def write_data(data):
    write_log_file(data, 'data.txt')

def write_log(message):
    write_log_file(message, 'log.txt')

def write_log_file(message, file):
    with open(file, "a") as f:
        f.write("{} {}\n".format(datetime.now(), message))

def compute_on_state(now):

    # if currently load shedding turn off
    try:

        next_load_shedding_start, next_load_shedding_end, stage = load_shedding_next_mins(now)
        
        if(next_load_shedding_start < (2 * 60)):
            write_log("Load shedding. OFF")
            return False

    except Exception as e:
        if(str(e) == 'No load shedding scheduled.'):
            write_log('No load shedding scheduled.')
        else:
            write_error(str(e))
            write_log("Error with load shedding schedule, fail safe. ON")
            return True # fail safe keep on   


    # if not load shedding check if night time
    # 6pm to 6am
   
    if(now.time() >= time(23,00) or now.time() <= time(6,00)):
        
        if(stage >=5):
            write_log("Night time, but stage " + stage + ". ON")
            return True
        
        # night time is off time
        write_log("Night time. OFF")
        return False
    

    # Otherwise is on
    write_log("No load shedding and is daytime. ON")
    return True




    
if __name__ == '__main__':

    try:
        d = tinytuya.OutletDevice(
            dev_id=os.getenv('DEV_ID'),
            address="Auto",  # Or set to 'Auto' to auto-discover IP address
            local_key=os.getenv('LOCAL_KEY'),
            version=3.3,
        )

        lookup =  {"1":"Switch 1","9":"Countdown 1","17":"Add Electricity","18":"Current","19":"Power","20":"Voltage","21":"Test Bit","22":"voltage coe","23":"electric coe","24":"power coe","25":"electricity coe","26":"Fault","38":"Relay Status","39":"Overcharge Switch","40":"Light Mode","41":"Child Lock","42":"Cycle Time","43":"Random Time","44":"Inching Switch"}

        data = d.status()

        data_string = ""

        for dps in data['dps']:
            data_string = data_string + '{}: {};'.format(lookup[str(dps)], data['dps'][dps])

        write_data(data_string)

        if(compute_on_state(datetime.now())):
            d.turn_on()
        else:
            d.turn_off()


    except Exception as e:
            write_log("Device offline.")
            write_error(e)


    try:

        next_load_shedding_start, next_load_shedding_end, stage = load_shedding_next_mins()
        write_log("Load shedding starts in {} hours, ends in {} hours.".format(next_load_shedding_start/60, next_load_shedding_end/60))

    except Exception as e:
        print(e)



     


## DPS Table
