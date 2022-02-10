import statistics
import itertools
import boto3
from boto3.dynamodb.conditions import Key, Attr

class DataBase:
    def __init__(self, table):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table)

    def ScanItems(self):
        self.response = self.table.scan()
        return self.response
        
    def PutItem(self,count,deviceid,datatype,minute,avg,min_value,max_value):
        self.table.put_item(
            Item={
                'index': count,
                'deviceid': deviceid,
                'datatype': datatype,
                'timestamp': minute,
                'Average': avg,
                'Min': min_value,
                'Max': max_value,
            }
        )
    
    def PutAlert(self,count,deviceid,datatype,minute,rule):
        self.table.put_item(
            Item={
                'index': count,
                'deviceid': deviceid,
                'datatype': datatype,
                'timestamp': minute,
                'rule': rule
            }
        )
        
    def Scan(self,type,min,max):
        response = self.table.scan(
            FilterExpression=Attr('datatype').eq(type) & (Attr('Max').gt(max) | Attr('Min').lt(min)) 
        )
        return response


