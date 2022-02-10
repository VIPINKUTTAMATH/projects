from model import UserModel, DeviceModel, WeatherDataModel, DailyReportModel
from datetime import datetime

def Print_If_Valid(model, result):
    if(result == -1):
        print('\t\t\t' + str(model.latest_error))
    else:
        print('\t\t\t'+ str(result))

print("\n********************User Data Model****************")
print("\tAccessing User model in Admin mode using user - admin")
user_coll = UserModel('admin')
print("\t\tFinding:")
user_document = user_coll.find_by_username('admin')
Print_If_Valid(user_coll,user_document)
print("\t\tInserting:")
user_document = user_coll.insert('test_3', 'test_3@example.com', 'default')
Print_If_Valid(user_coll,user_document)

print("\n\tAccessing User model in default mode using user - user_1")
user_coll = UserModel('user_1')
print("\t\tFinding:")
user_document = user_coll.find_by_username('admin')
Print_If_Valid(user_coll,user_document)
print("\t\tInserting:")
user_document = user_coll.insert('test_4', 'test_4@example.com', 'default')
Print_If_Valid(user_coll,user_document)


print("\n********************Device Data Model****************")
print("\nInsert on device (DT002) shows different error based on role of user")
print("\tAccessing Device model in admin mode using user - admin")
device_coll = DeviceModel('admin')
print("\t\tFinding:")
device_document = device_coll.find_by_device_id('DT002')
if (device_document):
    print('\t\t\t'+str(device_document))

print("\t\tInserting:")
device_document = device_coll.insert('DT002', 'Temperature Sensor', 'Temperature', 'Acme',{'admin':'rw', 'default':'r'})
Print_If_Valid(device_coll,device_document)

print("\tAccessing Device model in admin mode using user - user_1")
device_coll = DeviceModel('user_1')
print("\t\tFinding:")
device_document = device_coll.find_by_device_id('DT002')
if (device_document):
    print('\t\t\t'+str(device_document))

print("\t\tInserting:")
device_document = device_coll.insert('DT002', 'Temperature Sensor', 'Temperature', 'Acme',{'admin':'rw', 'default':'r'})
Print_If_Valid(device_coll,device_document)


print("\n********************Whether Data Model****************")
print("\nSearch and insert on device (DT002) support rw in admin mode and r in default mode")
print("\tCase1: User admin (role is admin)")
wdata_coll = WeatherDataModel('admin')
print("\t\tSearching:")
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print('\t\t\t'+str(wdata_document))

print("\t\tInserting:")
wdata_document = wdata_coll.insert('DT002', 12, datetime(2021, 12, 2, 13, 30, 0))
Print_If_Valid(wdata_coll,wdata_document)

print("\n\tCase2: User user_1 (role is default)")
wdata_coll = WeatherDataModel('user_1')
print("\t\tSearching:")
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print('\t\t\t'+str(wdata_document))

print("\t\tInserting:")
# Shows a failed attempt on how to insert a new data point
wdata_document = wdata_coll.insert('DT002', 12, datetime(2021, 11, 2, 13, 30, 0))
Print_If_Valid(wdata_coll,wdata_document)

print("\nSearch and insert on device (DT003) support rw in admin mode and rw in default mode")
print("\tCase1: User admin (role is admin)")
wdata_coll = WeatherDataModel('admin')
print("\t\tSearching:")
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT003', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print('\t\t\t'+str(wdata_document))

print("\t\tInserting:")
wdata_document = wdata_coll.insert('DT003', 12, datetime(2021, 12, 2, 13, 30, 0))
Print_If_Valid(wdata_coll,wdata_document)

print("\n\tCase2: User user_1 (role is default)")
wdata_coll = WeatherDataModel('user_1')
print("\t\tSearching:")
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT003', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print('\t\t\t'+str(wdata_document))

print("\t\tInserting:")
# Shows a failed attempt on how to insert a new data point
wdata_document = wdata_coll.insert('DT003', 12, datetime(2021, 11, 2, 13, 30, 0))
Print_If_Valid(wdata_coll,wdata_document)


#AGGREGATION
print("\n********************Daily Report Model****************")
report = DailyReportModel()
report.update_data()
print("\nData for DT003 in a range 2020/12/02 to 2021/12/02 using Daily Report Model")
daily_data = report.find_by_device_and_date_range('DT003',datetime(2020, 12, 2),datetime(2021, 12, 2))
if(daily_data):
    for item in daily_data:
        print(item)

print("\nData for DT002 in a range 2021/06/02 to 2022/12/02 using Daily Report Model")
daily_data = report.find_by_device_and_date_range('DT002',datetime(2021, 6, 2),datetime(2022, 12, 2))
if(daily_data):
    for item in daily_data:
        print(item)
