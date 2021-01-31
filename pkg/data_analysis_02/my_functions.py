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


import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import calendar

def get_months_dates(month, year):
    # This returns list of dates of specified lengths of months.
    lst = []
    for i in range(0, calendar.monthrange(year, month)[1]): 
        date_ = datetime.date(year, month, 1)
        date = date_ + datetime.timedelta(days=i)
        lst.append(date.strftime("%m/%d/%Y"))
    return lst


import requests

def json_get_sales_count(obj):
    """Recursively fetch values from nested JSON."""
    arr = {'bakedgoods': {}, 'breakfast': {}, 'lunch': {}}
    itemvalue = None
    categoryname = None
    itemname = None

    def extract(obj, arr, itemvalue, categoryname, itemname):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, itemvalue, categoryname, itemname)
                elif k == 'item':
                    itemkey = v
                elif k == 'soldQuantity':
                    itemvalue = v
                elif k == 'categoryName':
                    if v == 'LUNCH':
                        categoryname = 'lunch'
                    elif v == 'BREAKFAST':
                        categoryname = 'breakfast'
                    elif v == 'BAKED GOODS':
                        categoryname = 'bakedgoods'
                elif k == 'productName':
                    v = v.replace(' + ', '')
                    v = v.replace('To Go', '')
                    v = v.replace('Sit In', '')
                    v = v.replace('/w Mixed Seeds, Nuts & Honey', '')
                    v = v.replace('/w Cranberries, Hazelnuts & Honey', '')
                    v = v.replace('/w Honey', '')
                    v = v.replace(', ', '')
                    v = v.replace('Not Heated', '')
                    v = v.replace('Heated', '')
                    v = v.replace('Soup & Sandwich', '')
                    v = v.replace('Ham Toastie', 'Ham & Cheese Toastie')
                    itemname = v

                if categoryname and itemvalue and itemname:
                    if itemname in arr[categoryname]:
                        arr[categoryname][itemname] += itemvalue
                    else:
                        arr[categoryname][itemname] = itemvalue
                    itemvalue = None
                    categoryname = None
                    itemname = None

        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, itemvalue, categoryname, itemname)
        return arr

    values = extract(obj, arr, itemvalue, categoryname, itemname)
    return values


def get_summary_report(token, startdate, enddate):
    arr = {
        'searchCriteria': {
            'startDate': startdate,
            'endDate': enddate,
            'includedReports': [102]
        }
    }
    result = requests.post(url='https://mapi-eu.talech.com/reports/receiptssummaryreport',
                           json=arr,
                           headers=token)
    items = result.json()
    salesdata = json_get_sales_count(items)
    return salesdata



def transform_category_to_num(category):
    catnum = 0
    if category == 'bakedgoods':
        catnum = 1
    elif category == 'breakfast':
        catnum = 2
    elif category == 'lunch':
        catnum = 3 
    return catnum