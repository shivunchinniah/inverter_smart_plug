import httpx
import csv
from dotenv import load_dotenv
import os
from datetime import date, datetime, timedelta
from dateutil import parser
import bisect
import pytz


load_dotenv()  # take environment variables from .env.
load_shedding_url = "https://github.com/beyarkay/eskom-calendar/releases/download/latest/machine_friendly.csv"


area = os.getenv("LOAD_SHEDDING_AREA")


def load_shedding_next_mins():

    # Pull from load shedding calendar

    schedule = []

    starts = []
    ends = []

    with httpx.stream("GET", load_shedding_url, follow_redirects=True) as r:
        for row in csv.reader(r.iter_lines()):
            if row[0] == area:
                schedule.append(row)
                starts.append(parser.parse(row[1]))
                ends.append(parser.parse(row[2]))


    starts.sort()
    ends.sort()


    now = datetime.now(tz=pytz.timezone(os.getenv('TIMEZONE'))) 
    index = bisect.bisect_left(ends, now) 

    if (index >= len(starts)):
        raise Exception("No load shedding scheduled.")

    start_mins = (starts[index]-now).total_seconds() / 60
    end_mins = (ends[index]-now).total_seconds() / 60

    return start_mins, end_mins





    
