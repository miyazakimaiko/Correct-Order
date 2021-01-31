import pandas as pd

class Weather:
    def __init__(self, datetime, temperature, weather_id):
        self.datetime = datetime
        self.temperature = temperature
        self.weather_id = weather_id
        
    def __iter__(self):
        yield self.temperature
        yield self.weather_id
        
    @classmethod
    def columns(cls):
        return['temperature', 'weather_id']
    

class AllWeather:
    def __init__(self):
        self.arr = {}
        
    def set_item(self, item):
        self.arr[item.datetime] = item
        
    def get_item(self, date):
        if date in self.arr:
            return self.arr[date]
        else:
            return False  
        
    @property
    def items(self):
        return pd.DataFrame(self.arr, index=Weather.columns())
    
    
    
class Date:
    def __init__(self, date):
        self.date = date
        self.dayofweek = pd.Timestamp(pd.to_datetime(date)).dayofweek
        self.holiday = 0
        
    def __iter__(self):
        yield self.date
        yield self.dayofweek
        yield self.holiday
        
    @classmethod
    def columns(cls):
        return['datetime', 'dayofweek', 'holiday']
    
    
class Product:    
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
            
    def __iter__(self):
        yield self.id
        yield self.name
        yield self.category
    
    @classmethod
    def columns(cls):
        return ['id', 'name', 'category']
    
    
class AllProduct:
    def __init__(self):
        self.arr = {}
        
    def set_item(self, item):
        self.arr[item.name] = item
        
    def get_item(self, name):
        if name in self.arr:
            return self.arr[name]
        else:
            return False
        
    @property
    def items(self):
        return pd.DataFrame(self.arr.values(), columns=Product.columns())
    
    
class Sales:
    def __init__(self, demand, product=None):
        self.product = product
        self.demand = demand
        
    def __iter__(self):
        yield self.product.name
        yield self.demand
        
    @classmethod
    def columns(cls):
        return['item_name', 'demand']
    
    
class ProductsSales:
    def __init__(self):
        self.arr = {}
        
    def set_item(self, sales):
        self.arr[sales.product.name] = sales.demand
        
    def get_item(self, name):
        if name in self.arr:
            return self.arr[name]
        else:
            return False
        
    def __iter__(self):
        for i in self.arr:
            yield self.arr[i]
    
    
class Trainingset:
    def __init__(self):
        self.arr = {}
        
    def set_demand(self, datetime, item):
        try:
            self.arr[datetime]['demand'] = item
        except:
            self.arr[datetime] = {'demand':item, 'weather':None, 'calendar':None}
        
    def set_weather(self, datetime, weather):
        try:
            self.arr[datetime]['weather'] = weather
        except:
            self.arr[datetime] = {'demand':None, 'weather':weather, 'calendar':None}
        
    def set_calendar(self, datetime, calendar):
        try:
            self.arr[datetime]['calendar'] = calendar
        except:
            self.arr[datetime] = {'demand':None, 'weather':None, 'calendar':calendar}
        
    def get_item(self, date, itemname):
        return self.arr[date]['demand'].arr[itemname]
        
    @property
    def items(self):
        demand = pd.DataFrame([item['demand'].arr for item in self.arr.values()])
        weather = pd.DataFrame([item['weather'] for item in self.arr.values()], columns=Weather.columns())
        calendar = pd.DataFrame([item['calendar'] for item in self.arr.values()], columns=Date.columns())
        df = pd.concat([calendar, weather, demand], axis=1, sort=False)
        return df.set_index('datetime')