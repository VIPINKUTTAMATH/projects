# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId
from datetime import datetime

class AccessManager:
    def __init__(self, username):
        self._db = Database()
        self._latest_error = ''
        key = {'username': username}
        user_document = self.__findUserDoc(key)
        self.role = user_document['role']
    
    # Private function (starting with __) to be used as the base for all find functions
    def __findUserDoc(self, key):
        user_document = self._db.get_single_data('users', key)
        return user_document
    
    def __findDeviceDoc(self, key):
        device_document = self._db.get_single_data('devices', key)
        return device_document

    def Is_admin(self):
        if self.role == 'admin':
            self._latest_error = ''
            return True
        return False
    
    def Find_Role(self):
        return self.role
    
    def Access_Type(self, deviceid):
        device_document = self.__findDeviceDoc({'device_id': deviceid})
        if (device_document):
            access_data = device_document.get('access', None)
            if(access_data):
                return access_data.get(self.role, None)
        return 'rw'

# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self,username):
        self.username = username
        self.accessMgr = AccessManager(username)
        if self.accessMgr.Is_admin():
            self._db = Database()
            self._latest_error = ''
        else:
            self._latest_error = 'UnAutherized Access by '+ username 
        
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        if not self.accessMgr.Is_admin():
            return -1
        key = {'username': username}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        if not self.accessMgr.Is_admin():
            return -1
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        if not self.accessMgr.Is_admin():
            return -1
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document
    
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role):
        if not self.accessMgr.Is_admin():
            return -1
        
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if (user_document):
            self._latest_error = f'Username {username} already exists'
            return -1
        
        user_data = {'username': username, 'email': email, 'role': role}
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)





# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self, username):
        self.username = username
        self.accessMgr = AccessManager(username)
        self._db = Database()
        self._latest_error = ''
        
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id):
        key = {'device_id': device_id}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer,access):
        if self.accessMgr.Access_Type(device_id) == 'rw':
            self._latest_error = ''
            device_document = self.find_by_device_id(device_id)
            if (device_document):
                self._latest_error = f'Device id {device_id} already exists'
                return -1
        
            device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer, 'access':access}
            device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
            return self.find_by_object_id(device_obj_id)
        else:
            self._latest_error = 'Unautherized access by ' + self.username
            return -1


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self, username):
        self.username = username
        self.accessMgr = AccessManager(username)
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        if self.accessMgr.Access_Type(device_id) == 'rw':
            self._latest_error = ''
            wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp)
            if (wdata_document):
                self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
                return -1
            
            weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
            wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
            return self.find_by_object_id(wdata_obj_id)
        else:
            self._latest_error = 'Unautherized access by ' + self.username
            return -1


class DailyReportModel:
    DAILY_REPORT_MODEL = 'daily_report_data'
    def __init__(self):
        self._db = Database()
        self._latest_error = ''
        
    def update_data(self):
        pipeline = [
            { "$group": {
                "_id": {
                    "device_id": "$device_id",
                    "date" : {"$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$timestamp"
                    }}
                },
                "avg": {"$avg": "$value"},
                "min": {"$min": "$value"},
                "max": {"$max": "$value"}
                }
            },

            {
                "$group": {
                "_id": "$_id.device_id",
                    "data": {
                        "$push":  { 
                            "date": "$_id.date", 
                            "min": "$min",
                            "avg": "$avg",
                            "max": "$max" 
                        }
                    }
                }
            }
        ]
        
        self._db.drop_collection(DailyReportModel.DAILY_REPORT_MODEL)
        result = list(self._db.aggregate_data('weather_data',pipeline))
        for item in result:
            self._db.insert_single_data(DailyReportModel.DAILY_REPORT_MODEL, item)

    def find_by_device_and_date_range(self,device_id, start, end):
        pipeline = [{
                "$match": { 
                    "_id": device_id
                }
            },
            {
                "$unwind": "$data" 
            },
            {
                "$addFields" : { "date" : {"$dateFromString": {
                        "format": "%Y-%m-%d",
                        "dateString": "$data.date"
                    }}}
            },
            { 
                "$unset": ["_id", "data.date"]
            },
            {
                "$match": { 
                    "date": { "$gt": start, "$lt": end }
                }
            }
        ]
        result = list(self._db.aggregate_data(DailyReportModel.DAILY_REPORT_MODEL,pipeline))
        return result

        #"values.date": { "$gt": start, "$lt": end }