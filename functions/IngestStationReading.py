from __future__ import print_function
import json

"""
Ingests a JSON string like:

    {
        "temp_dewpt": "10.8",
        "rain_day": "0",
        "rain": "0",
        "wind_ave": "0.30",
        "hum_in": "70",
        "temp_out": "17.2",
        "wind_dir": "90",
        "hum_out": "66",
        "wind_gust": "1.00",
        "temp_apprt": "17.3",
        "wind_chill": "17.2",
        "tdate": "2016-10-25",
        "temp_in": "19.3",
        "abs_pressure": "1018.0000",
        "ttime": "10%3A03%3A29"
    }

"""

print('Loading function')

def lambda_handler(event, context):
    try:
        print("temp_dewpt = " + event['temp_dewpt'])
        print("rain_day = " + event['rain_day'])
        print("rain = " + event['rain'])
        print("wind_ave = " + event['wind_ave'])
        print("hum_in = " + event['hum_in'])
        print("temp_out = " + event['temp_out'])
        print("wind_dir = " + event['wind_dir'])
        print("hum_out = " + event['hum_out'])
        print("wind_gust = " + event['wind_gust'])
        print("temp_apprt = " + event['temp_apprt'])
        print("wind_chill = " + event['wind_chill'])
        print("tdate = " + event['tdate'])
        print("temp_in = " + event['temp_in'])
        print("abs_pressure = " + event['abs_pressure'])
        print("ttime = " + event['ttime'])
        readingts = '{0}{1}'.format(
            event['tdate'].replace('-', ''), event['ttime'].replace('%3A', '')
            )
    except KeyError:
        return 'Failed to insert data'
    else:
        return 'Done, entered data for {0}'.format(readingts)