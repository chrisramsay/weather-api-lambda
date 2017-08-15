"""
AWS Lambda code base for the weather-api
"""

import os
import logging
import pymysql

def get_connection():
    # Connect to the database
    return pymysql.connect(
        host=os.environ['host'],
        user=os.environ['user'],
        password=os.environ['password'],
        db=os.environ['db'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_last_climate_reading_ts(event, context):
    """
    Return timestamp of last climate reading in database
    """
    logging.getLogger().setLevel(logging.INFO)
    return last_climate()

def get_last_soil_reading_ts(event, context):
    """
    Return timestamp of last soil temperature station reading in database
    """
    logging.getLogger().setLevel(logging.INFO)
    return last_soil()

def process_weather_station(data):
    """
    Processes handled weather station data
    """
    try:
        # Get the keys in order
        keys = [f for f in iter(data.keys())]
        keys.sort()
        insert_data = [data.get(f, 'NULL') for f in keys]
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `station` (`abs_pressure`, `hum_in`, `hum_out`, `rain`, `rain_day`, `tdate`, `temp_apprt`, `temp_dewpt`, `temp_in`, `temp_out`, `ttime`, `wind_ave`, `wind_chill`, `wind_dir`, `wind_gust`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (insert_data))
            connection.commit()
        finally:
            connection.close()
    except:
        return 'FAIL'
    else:
        return None

def process_climate(data):
    """
    Processes handled climate monitoring data
    """
    try:
        # Get the keys in order
        keys = [f for f in iter(data.keys())]
        keys.sort()
        insert_data = [data.get(f, 'NULL') for f in keys]
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `climate` (`airflow`, `humidity`, `light`, `sound`, `tdate`, `temp`, `ttime`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (insert_data))
            connection.commit()
        finally:
            connection.close()
    except:
        return 'FAIL'
    else:
        return None

def process_soil_temps(data):
    """
    Processes handled soil temperature station data
    """
    try:
        # Get the keys in order
        keys = [f for f in iter(data.keys())]
        keys.sort()
        print(keys)
        insert_data = [data.get(f, 'NULL') for f in keys]
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `soil_temps` (`temp_concrete`, `temp_grass`, `soil_d`, `soil_m`, `soil_s`, `temp_system`, `tdate`, `ttime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                print(sql)
                print(insert_data)
                cursor.execute(sql, (insert_data))
            connection.commit()
        finally:
            connection.close()
    except:
        return 'FAIL'
    else:
        return None

def last_climate():
    """
    Get last climate reading timestamp
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
        SELECT concat(s.tdate, ' ', MAX(s.ttime)) AS lastreading
        FROM   (SELECT tdate,
                       ttime
                FROM   climate
                WHERE  tdate = (SELECT MAX(tdate)
                                FROM `climate`)) AS s
        """
        cursor.execute(sql)
        data = cursor.fetchone()
    except:
        return 'FAIL'
    else:
        return data['lastreading']
    finally:
        connection.close()

def last_soil():
    """
    Get last soil temperature reading timestamp
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
        SELECT concat(s.tdate, ' ', MAX(s.ttime)) AS lastreading
        FROM   (SELECT tdate,
                       ttime
                FROM   soil_temps
                WHERE  tdate = (SELECT MAX(tdate)
                                FROM `soil_temps`)) AS s
        """
        cursor.execute(sql)
        data = cursor.fetchone()
    except:
        return 'FAIL'
    else:
        return data['lastreading']
    finally:
        connection.close()

################################################################################
#                               LAMBDA HANDLERS                                #
################################################################################

def post_weather_station(event, context):
    """
    Weather station data ingestion handler
    """
    message = event['query']
    logging.getLogger().setLevel(logging.INFO)
    return process_weather_station(message)

def post_climate(event, context):
    """
    Climate system data ingestion handler
    """
    message = event['query']
    logging.getLogger().setLevel(logging.INFO)
    return process_climate(message)

def post_soil_temps(event, context):
    """
    Soil temperature station data ingestion handler
    """
    message = event['query']
    logging.getLogger().setLevel(logging.INFO)
    return process_soil_temps(message)
