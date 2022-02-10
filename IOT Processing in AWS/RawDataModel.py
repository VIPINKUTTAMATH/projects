
import itertools
from DataBase import DataBase

class RawDataModel:
    def __init__(self):
        self.db = DataBase('BSM_RAW_DATA')
        self.response = self.db.ScanItems()
    
    def ForEachMinuteAndDevice(self,callback):
        items_by_deviceid = itertools.groupby(
            self.response["Items"], 
            key=lambda x: x["deviceid"]
        )
        
        for deviceid, items in items_by_deviceid:
        # Group the response by items per minute
            items_by_minute = itertools.groupby(
                items, 
                key=lambda x: x["timestamp"][:16]  #The first 16 characters including the minute
            )
            
            # Calculate the statistics for each minute
            for minute, items in items_by_minute:
                items = sorted(items, key = lambda i: i['datatype'])
                items_by_type = itertools.groupby(
                    items, 
                    key=lambda x: x["datatype"]
                )
                
                for datatype, items in items_by_type:
                    callback(deviceid,datatype,minute,items)