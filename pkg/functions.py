import datetime


def get_last_7days():
    lastweek = []

    for i in range(-7, 1, 1):
        d = datetime.date.today() + datetime.timedelta(days=i)
        lastweek.append(d.strftime("%m/%d/%Y 00:00:00"))
    return lastweek


def get_recent_week_nums():
    weeks = []
    for i in range(1, 36, 7):
        w = datetime.date.today() + datetime.timedelta(days=i)
        week = w.strftime("%V")
        weeks.append(week)
    return weeks


import os
import secrets
from PIL import Image
from . import app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/avatar', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def json_get_fooditem_keys(obj):
    """Recursively fetch values from nested JSON and extract item name and key"""
    arr = {}
    itemname = 'No name'
    itemkey = 'no-key'
    itemlabel = 'no-label'
    category = 'no-category'

    def extract(obj, arr, itemname, itemkey, itemlabel, category):
        """Recursively search for values of key in JSON tree."""

        def getLabel(obj):
            """This labels identify the difference of items which hold same item name"""
            l = 'no-label'
            for item in obj:
                for k, v in item.items():
                    if k == 'label':
                        if v != 'Tall' and v != 'Reg' \
                                and v != 'To Go' and v != 'Sit In' \
                                and v != 'Heated' and v != 'Not Heated':
                            l = v
                    else:
                        pass
            return l

        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'items':
                    extract(v, arr, itemname, itemkey, itemlabel, category)
                elif k == 'productVariants':
                    extract(v, arr, itemname, itemkey, itemlabel, category)
                elif k == 'modifierOptions':
                    itemlabel = getLabel(v)
                elif k == 'skuNumber':
                    itemkey = v
                elif k == 'name':
                    itemname = v
                elif k == 'categoryType':
                    category = v
                arr[itemkey] = {'name': itemname, 'label': itemlabel, 'category': category}

        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, itemname, itemkey, itemlabel, category)
        return arr

    def bundle_same_items(obj, category):
        """extract keys of items which belong to specific category"""
        arr = {}
        itemkey = None
        itemname = None
        itemlabel = None

        def get_similar_string(str1, str2):
            """if str2 contains str1, return str2.
            This return str2 even words' order doesn't match"""
            count = 0
            words = str1.split(' ')
            for w in words:
                if w in str2:
                    count += 1
            if count == len(words):
                return str2
            else:
                return False

        for key, val in obj.items():
            for k, v in val.items():
                if k == 'category':
                    if v == category:
                        itemkey = key
                    else:
                        continue
                elif k == 'name':
                    if v == 'Soup & Sandwich':
                        """These items cannot be identified its sandwich name by its name.
                        Instead, we need to use labels for that"""
                        continue
                    else:
                        itemname = v
                elif k == 'label':
                    if v != 'no-label':
                        itemlabel = v
                    else:
                        pass

            if itemname and itemkey:
                try:
                    for key, value in arr.items():
                        name = get_similar_string(itemname, key)
                        if name:
                            k = name
                            break
                    arr[k].append(itemkey)
                except:
                    arr[itemname] = [itemkey]

            elif itemlabel and itemkey:
                try:
                     for key, value in arr.items():
                         name = get_similar_string(itemlabel, key)
                         if name:
                             k = name
                             break
                     arr[k].append(itemkey)
                except:
                    arr[itemlabel] = [itemkey]

            itemkey = None
            itemname = None
            itemlabel = None

        return arr

    values = extract(obj, arr, itemname, itemkey, itemlabel, category)
    lunch = bundle_same_items(values, 'LUNCH')
    baked = bundle_same_items(values, 'BAKED GOODS')
    breakfast = bundle_same_items(values, 'BREAKFAST')
    bundled = {'LUNCH': lunch, 'BAKED GOODS': baked, 'BREAKFAST': breakfast}
    return bundled


def json_get_sales_count(obj):
    """Recursively fetch values from nested JSON."""
    arr = {'BAKED GOODS': {}, 'BREAKFAST': {}, 'LUNCH': {}}
    itemkey = None
    itemvalue = None
    categoryname = None

    def extract(obj, arr, itemkey, itemvalue, categoryname):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, itemkey, itemvalue, categoryname)
                elif k == 'item':
                    itemkey = v
                elif k == 'soldQuantity':
                    itemvalue = v
                elif k == 'categoryName':
                    if v == 'LUNCH' or v == 'BREAKFAST' or v == 'BAKED GOODS':
                        categoryname = v

                if categoryname and itemkey and itemvalue:
                    arr[categoryname][itemkey] = itemvalue
                    itemkey = None
                    itemvalue = None
                    categoryname = None

        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, itemkey, itemvalue, categoryname)
        return arr

    values = extract(obj, arr, itemkey, itemvalue, categoryname)
    return values


def merge_data(salesdata, itemdata):
    arr = {}

    for date, dailysale in salesdata.items():
        """Create empty ditionaries for each date which contain sorted item keys"""
        arr[date] = {}
        for category, items in itemdata.items():
            arr[date][category] = {}
            for itemname, itemkeys in items.items():
                arr[date][category][itemname] = {}
                mainkey = None
                subkeys = []
                for key in itemkeys:
                    if mainkey is None or len(mainkey) > len(key):
                        mainkey = key
                    else:
                        subkeys.append(key)

                if mainkey:
                    arr[date][category][itemname][mainkey] = subkeys
                    arr[date][category][itemname]['sold'] = 0

        for soldcategory, solditems in dailysale.items():
            """Find the matching keys in the array which was created earlier,
            and save sales quantity in the array"""
            for soldkey, soldnum in solditems.items():
                for soldname, soldkeys in arr[date][soldcategory].items():
                    for parentkey, subkeys in soldkeys.items():
                        if parentkey == soldkey:
                            arr[date][soldcategory][soldname]['sold'] += soldnum
                        elif isinstance(subkeys, list):
                            for key in subkeys:
                                if key == soldkey:
                                    arr[date][soldcategory][soldname]['sold'] += soldnum
                                    # arr[date][soldcategory][soldname][parentkey] += soldnum

        # def addUpSameItems(array):
        #     name = None
        #     total = 0
        #     for date, dailysale in array.items():
        #         for category, solditems in dailysale.items():
        #             for itemname, itemkeys in solditems.items():
        #                 for itemkey, soldnum in itemkeys.items():
        #                     if name is None:
        #                         name = itemkey
        #                     total += soldnum
        #                 array[date][category][itemname][name] = total
        #                 total = 0
        #                 name = None
        #
        # addUpSameItems(arr)
    return arr