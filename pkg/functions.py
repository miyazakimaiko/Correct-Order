def jsonGetFoodItemkeys(obj):
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

    def bundleSameItems(obj, category):
        """extract keys of items which belong to specific category"""
        arr = {}
        itemkey = None
        itemname = None
        itemlabel = None

        def getSimilarString(str1, str2):
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

            if itemname:
                try:
                    for key, value in arr.items():
                        name = getSimilarString(itemname, key)
                        if name:
                            k = name
                            break
                    arr[k][itemkey] = 0
                except:
                    arr[itemname] = {itemkey: 0}

            elif itemlabel:
                try:
                     for key, value in arr.items():
                         name = getSimilarString(itemlabel, key)
                         if name:
                             k = name
                             break
                     arr[k][itemkey] = 0
                except:
                    arr[itemlabel] = {itemkey: 0}

            itemkey = None
            itemname = None
            itemlabel = None

        return arr

    values = extract(obj, arr, itemname, itemkey, itemlabel, category)
    lunch = bundleSameItems(values, 'LUNCH')
    baked = bundleSameItems(values, 'BAKED GOODS')
    breakfast = bundleSameItems(values, 'BREAKFAST')
    bundled = {'LUNCH': lunch, 'BAKED GOODS': baked, 'BREAKFAST': breakfast}
    return bundled


def jsonGetSalesCount(obj, name, key, value):
    """Recursively fetch values from nested JSON."""
    arr = {}
    itemname = 'No name'
    itemkey = 'no-key'
    itemvalue = 0

    def extract(obj, arr, itemname, itemkey, itemvalue, name, key, value):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, itemname, itemkey, itemvalue, name, key, value)
                elif k == name:
                    itemname = v
                elif k == key:
                    itemkey = v
                elif k == value:
                    itemvalue = v
                arr[itemname] = {key: itemkey, value: itemvalue}

        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, itemname, itemkey, itemvalue, name, key, value)
        return arr

    values = extract(obj, arr, itemname, itemkey, itemvalue, name, key, value)
    return values
