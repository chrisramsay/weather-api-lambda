"""
AWS Lambda code base for the weather-api.
"""

import os
import logging
import pymysql

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

STATION_SQL = """
INSERT INTO `station`
    (`abs_pressure`, `hum_in`, `hum_out`, `rain`, `rain_day`, `tdate`,
    `temp_apprt`, `temp_dewpt`, `temp_in`, `temp_out`, `ttime`, `wind_ave`,
    `wind_chill`, `wind_dir`, `wind_gust`)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

SOIL_TEMPS_SQL = """
INSERT INTO `soil_temps`
    (`temp_concrete`, `temp_grass`, `soil_d`, `soil_m`, `soil_s`, `temp_system`,
    `tdate`, `ttime`)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)
"""

CLIMATE_SQL = """
INSERT INTO `climate`
    (`airflow`, `humidity`, `light`, `sound`, `tdate`, `temp`, `ttime`)
VALUES
    (%s, %s, %s, %s, %s, %s, %s)
"""

NETSPEED_SQL = """
INSERT INTO `netspeed`
    (`bytes_received`, `bytes_sent`, `cc`, `country`, `d`, `download`, `host`, 
    `lat`, `latency`, `lon`, `name`, `ping`, `server_id`, `sponsor`, `tdate`,
    `ttime`,`upload`, `url`, `url2`) 
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

################################################################################
#                              UTILITY FUNCTIONS                               #
################################################################################

def get_connection():
    """
    Returns a connection to the database
    """
    return pymysql.connect(
        host=os.environ['host'],
        user=os.environ['user'],
        password=os.environ['password'],
        db=os.environ['db'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def process_reading(data, sql_template):
    """
    Processes handled weather station data using data and SQL template
    parameters
    """
    try:
        LOGGER.info('Processing data: {}'.format(data))
        LOGGER.info('Received template: {}'.format(sql_template))
        # Get the keys in order
        keys = [f for f in iter(data.keys())]
        keys.sort()
        insert_data = [data.get(f, 'NULL') for f in keys]
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_template, (insert_data))
            connection.commit()
        finally:
            connection.close()
    except Exception as exc:
        LOGGER.error('Exception occurred: {0}'.format(exc))
        return 'FAIL'
    else:
        LOGGER.info('Processed data successfully for [{0} {1}]'.format(
            data['tdate'], data['ttime']))
        return None

def last_reading(table):
    """
    Get last reading timestamp from table parameter
    """
    LOGGER.info('Getting last TS from {}'.format(table))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
        SELECT concat(s.tdate, ' ', MAX(s.ttime)) AS lastreading
        FROM   (SELECT tdate,
                       ttime
                FROM   {0}
                WHERE  tdate = (SELECT MAX(tdate)
                                FROM `{0}`)) AS s
        """.format(table)
        cursor.execute(sql)
        data = cursor.fetchone()
    except Exception as exc:
        LOGGER.error('Exception occurred: {0}'.format(exc))
        return 'FAIL'
    else:
        LOGGER.info('Processed data successfully for {0}'.format(
            data['lastreading']))
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
    return process_reading(event['query'], STATION_SQL)

def post_climate(event, context):
    """
    Climate system data ingestion handler
    """
    return process_reading(event['query'], CLIMATE_SQL)

def post_soil_temps(event, context):
    """
    Soil temperature station data ingestion handler
    """
    return process_reading(event['query'], SOIL_TEMPS_SQL)

def get_last_climate_reading_ts(event, context):
    """
    Return timestamp of last climate reading in database
    """
    return last_reading('climate')

def get_last_soil_reading_ts(event, context):
    """
    Return timestamp of last soil temperature station reading in database
    """
    return last_reading('soil_temps')

def get_last_netspeed_reading_ts(event, context):
    """
    Return timestamp of last speed test reading in database
    """
    return last_reading('netspeed')

def post_netspeed(event, context):
    """
    Speed test data ingestion handler
    """
    return process_reading(event['query'], NETSPEED_SQL)
