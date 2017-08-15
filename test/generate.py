#!/usr/bin/env python

import json
import random
import time
import datetime

"""
Generates a fake weather reading, like:

{
  "data": {
    "abs_pressure": 1018,
    "hum_in": 70,
    "hum_out": 66,
    "rain": 0,
    "rain_day": 0,
    "tdate": "2016-10-25",
    "temp_apprt": 17.3,
    "temp_dewpt": 10.8,
    "temp_in": 19.3,
    "temp_out": 17.2,
    "ttime": "10:03:29",
    "wind_ave": 0.3,
    "wind_chill": 17.2,
    "wind_dir": 90,
    "wind_gust": 1
  }
}
"""

NOW = datetime.datetime.now()

def rand_two():
    return random.randint(10,99)

def rand_threefour():
    return random.randint(990,1030)

def rand_float():
    return round(random.randint(1,30) + random.random(), 1)

def date_today():
    return str(datetime.date.today())

def time_now():
    return NOW.strftime("%H:%M:%S")

def readingts():
    return NOW.strftime("%Y%m%d%H%M%S")

def timestamp():
    return int(time.time())

def generate():
    out = {}
    out['data'] = {}
    out['data']['abs_pressure'] = rand_threefour()
    out['data']['hum_in'] = rand_two()
    out['data']['hum_out'] = rand_two()
    out['data']['rain'] = rand_two()
    out['data']['rain_day'] = rand_two()
    out['data']['tdate'] = date_today()
    out['data']['temp_apprt'] = rand_float()
    out['data']['temp_dewpt'] = rand_float()
    out['data']['temp_in'] = rand_float()
    out['data']['temp_out'] = rand_float()
    out['data']['ttime'] = time_now()
    out['data']['wind_ave'] = rand_float()
    out['data']['wind_chill'] = rand_float()
    out['data']['wind_dir'] = rand_two()
    out['data']['wind_gust'] = rand_two()
    #out['readingts'] = readingts()
    #out['timestamp'] = timestamp()
    return json.dumps(out)

if __name__ == "__main__":
    print generate()
