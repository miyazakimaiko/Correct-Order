import os
import sys
import requests
import json
import pandas as pd
from datetime import datetime, date, timedelta, timezone
import s3fs

AWS_REGION = os.environ['region']
projectId = os.environ['projectId']
processed_folder = "processed"
startTime = datetime.now()
s3 = s3fs.S3FileSystem(anon=False)

def lambda_handler(event, context):

    for record in event['Records']:
        # Create some variables that make it easier to work with the data in the
        # event record.
        bucket = record['s3']['bucket']['name']
        api_key = '...'
        url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
        yesterday = datetime.now() - timedelta(days=1)
        timestamp = round(datetime.timestamp(yesterday))
        params = {
            'lat': '53.349805',
            'lon': '-6.26031',
            'units': 'metric',
            'dt': timestamp,
            'appid': api_key
        }
        # Fetch hourly weather data in Dublin from OpenWeatherMap API
        input_file = requests.get(url=url, params=params)
        output_file_name = os.path.splitext(os.path.basename(input_file))[0] + "_processed.csv"
        processed_subfolder = os.path.basename(input_file).split("__part",1)[0]
        output_fullpath = os.path.join(bucket,processed_folder,processed_subfolder,output_file_name)
        # Start the function that processes the incoming data.
        process_incoming_file(input_file, output_fullpath)

def process_incoming_file(input_file, output_file):
    result_json = input_file.json()
    # Flatten hourly weather data that are nested 
    result_df = pd.json_normalize(result_json['hourly'])
    weather_data = pd.json_normalize(data=result_json['hourly'], record_path='weather',
                                    meta=['dt', 'temp', 'feels_like', 'clouds'])
    weather_data = weather_data.drop(['main', 'description', 'icon', 'temp', 'clouds'], 1)
    weather_data['dt'] = weather_data['dt'].apply(lambda x: datetime.fromtimestamp(x))
    date = weather_data['dt'][0].strftime("%m-%d-%Y")
    weather_data['dt'] = weather_data['dt'].apply(lambda x: x.strftime("%m/%d/%Y %H:%M:%S"))
    weather_data = weather_data.drop(weather_data.index[21:])
    weather_data = weather_data.drop(weather_data.index[:6])
    return weather_data

