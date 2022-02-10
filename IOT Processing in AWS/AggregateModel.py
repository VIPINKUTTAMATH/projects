from DataBase import DataBase
import statistics

class AggregateModel:
    def __init__(self):
        self.db = DataBase('bsm_agg_data')
        self.counter = 1

    def UpdateAggregate(self,deviceid,datatype,minute,items):
        values_per_minute = [item["value"] for item in items]        
        avg = statistics.mean(values_per_minute)
        min_value = min(values_per_minute)
        max_value = max(values_per_minute)
        print(f" DevId: {deviceid}, datatype: {datatype} timestamp: {minute} / Average {avg} / Min {min_value} / Max {max_value}")
        self.db.PutItem(self.counter,deviceid,datatype,minute,avg,min_value,max_value)
        self.counter = self.counter+1