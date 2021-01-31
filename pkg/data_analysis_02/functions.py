import datetime
import requests
from dateutil.relativedelta import relativedelta
import calendar
import pandas as pd

def get_accesstoken(client_id, client_secret, refresh_token, client_version, token_url):
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'client_version': client_version
    }
    resp = requests.post(url=token_url,
                         json=data)
    resp_json = resp.json()
    return resp_json['access_token']