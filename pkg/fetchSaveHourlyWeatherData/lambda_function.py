import os
import sys
import requests
import json
import pandas as pd
from datetime import datetime, date, timedelta, timezone
import s3fs
import boto3
import csv

AWS_REGION = os.environ['AWS_REGION']
startTime = datetime.now()
s3 = s3fs.S3FileSystem(anon=False)

def lambda_handler(event, context):
    print(event)
    # Create some variables that make it easier to work with the data in the
    # event record.
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
    result_json = input_file.json()
    # Flatten hourly weather data that are nested 
    weather_data = pd.json_normalize(data=result_json['hourly'], record_path='weather',
                                    meta=['dt', 'temp', 'feels_like', 'clouds'])
    weather_data = weather_data.drop(['main', 'description', 'icon', 'temp', 'clouds'], 1)
    weather_data['dt'] = weather_data['dt'].apply(lambda x: datetime.fromtimestamp(x))
    date = weather_data['dt'][0].strftime("%m-%d-%Y")
    weather_data['dt'] = weather_data['dt'].apply(lambda x: x.strftime("%m/%d/%Y %H:%M:%S"))
    weather_data = weather_data.drop(weather_data.index[21:])
    weather_data = weather_data.drop(weather_data.index[:6])
    csv_data = weather_data.to_csv()

    #properly call your s3 bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hourlyweatherbucket')
    key = '{}.csv'.format(date)

    #Only then you can write the data into the '/tmp' folder.
    with open("/tmp/{}.csv".format(date), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(csv_data)
    #upload the data into s3
    bucket.upload_file("/tmp/{}.csv".format(date), key)