import tinytuya
import time
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.




try:


    d = tinytuya.OutletDevice(
        dev_id=os.getenv('DEV_ID'),
        address="Auto",  # Or set to 'Auto' to auto-discover IP address
        local_key=os.getenv('LOCAL_KEY'),
        version=3.3,
    )


    lookup =  {"1":"Switch 1","9":"Countdown 1","17":"Add Electricity","18":"Current","19":"Power","20":"Voltage","21":"Test Bit","22":"voltage coe","23":"electric coe","24":"power coe","25":"electricity coe","26":"Fault","38":"Relay Status","39":"Overcharge Switch","40":"Light Mode","41":"Child Lock","42":"Cycle Time","43":"Random Time","44":"Inching Switch"}

    data = d.status()

    for dps in data['dps']:
        print('{}: {}'.format(lookup[str(dps)], data['dps'][dps]))


except Exception as e:
        print(e)


## DPS Table
