from DataBase import DataBase
import itertools
from datetime import datetime
from datetime import timedelta

class AlertDataModel:
    def __init__(self):
        self.db = DataBase('bsm_alerts')
        self.counter = 1
    
    def CheckRule(self,type,min,max,count,rule):
        db = DataBase('bsm_agg_data')
        response = db.Scan(type,min,max)
        items = response['Items']
        items = sorted(items, key = lambda i: i['deviceid'])
        items_by_deviceid = itertools.groupby(
            items, 
            key=lambda x: x["deviceid"]
        )
        
        for deviceid, items in items_by_deviceid:
            devItems  = list(items)
            devItems = sorted(devItems, key = lambda i: i['timestamp'])
            for index, devItem in enumerate(devItems):
                start = datetime.strptime(devItem['timestamp'], "%Y-%m-%d %H:%M")
                finalIndex = index + count-1
                if finalIndex >= len(devItems):
                    break
                
                end = datetime.strptime(devItems[finalIndex]['timestamp'], "%Y-%m-%d %H:%M")
                calc = start + timedelta(minutes=count-1)   
                if end == calc:
                    curr = devItems[index]
                    print(f" Alert for device_id : {curr['deviceid']} starting at {curr['timestamp']}")
                    self.db.PutAlert(self.counter,curr['deviceid'],type,curr['timestamp'],rule)
                    self.counter = self.counter +1
'''                    for i in range(index,finalIndex+1):
                        print(devItems[i])'''

