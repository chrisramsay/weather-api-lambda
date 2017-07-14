"""
Ingests a JSON string like:

{
  "data": {
    "hum_out": 72,
    "wind_ave": 23.3,
    "wind_gust": 74,
    "temp_dewpt": 29.3,
    "temp_apprt": 11.3,
    "wind_chill": 1.5,
    "tdate": "2016-12-23",
    "rain": 70,
    "rain_day": 74,
    "abs_pressure": 1018,
    "hum_in": 84,
    "temp_out": 6,
    "ttime": "10:29:54",
    "temp_in": 18.5,
    "wind_dir": 79
  }
}
"""

import os
import logging
import pymysql

def lambda_process_handler(event, context):
    message = event['data']
    logging.getLogger().setLevel(logging.INFO)
    print(process_reading(message))

def process_reading(data):
    try:
        for key, val in data.items():
            if isinstance(val) is float:
                data[key] = int(val*100)
        # Get the keys in order
        keys = [f for f in iter(data.keys())]
        keys.sort()
        insert_data = [data.get(f, 'NULL') for f in keys]
        # Connect to the database
        connection = pymysql.connect(host=os.environ['host'],
                                     user=os.environ['user'], password=os.environ['password'],
                                     db=os.environ['db'], charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `weather` (`abs_pressure`, `hum_in`, `hum_out`, `rain`, `rain_day`, `tdate`, `temp_apprt`, `temp_dewpt`, `temp_in`, `temp_out`, `ttime`, `wind_ave`, `wind_chill`, `wind_dir`, `wind_gust`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (insert_data))
            connection.commit()
        finally:
            connection.close()
    except KeyError:
        return 'Failed to insert data'
    else:
        return 'Done'
