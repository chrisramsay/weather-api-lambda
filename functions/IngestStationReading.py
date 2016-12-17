from __future__ import print_function
import logging, boto3, json

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

TABLE = 'station'
REGION = 'eu-west-1'

def lambda_handler(event, context):
    logging.getLogger().setLevel(logging.INFO)
    print(process_reading(event))

def process_reading(event_data):
    """
    Table has the format:
        Primary partition key - readingts (String)
        Primary sort key - timestamp (Number)
    """
    tbl = boto3.resource('dynamodb', region_name=REGION).Table(TABLE)
    try:
        readingts = '{0}{1}'.format(
            event['tdate'].replace('-', ''), event['ttime'].replace('%3A', '')
            )
    except KeyError:
        return 'Failed to insert data'
    else:
        return 'Done, entered data for {0}'.format(readingts)
