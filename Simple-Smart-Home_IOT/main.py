import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.25  

print("Smart Home Simulation started.")
# Creating the edge-server for the communication with the user

def callback(n):
    print("Main: ", n)

edge_server_1 = Edge_Server('edge_server_1',callback)
time.sleep(WAIT_TIME)

# Creating the light_device
print("\n***************************************************************" )
print("Intitate the device creation and registration process. \n" )
print("Creating the Light devices for their respective rooms.")
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)  
light_device_2 = Light_Device("light_2", "Kitchen")
time.sleep(WAIT_TIME)  

# Creating the ac_device  
print("\n***************************************************************" )
print("Creating the AC devices for their respective rooms. ")
ac_device_1 = AC_Device("ac_1", "BR1")
ac_device_2 = AC_Device("ac_2", "Kitchen")
time.sleep(WAIT_TIME)  

print("\n***************************************************************" )
print("Get status of all devices.")
edge_server_1.get_status("all")
time.sleep(WAIT_TIME)

print("\n***************************************************************" )
print("Updating light_1 light_intensity to HIGH.")
edge_server_1.set("light_1","light_intensity","HIGH")
time.sleep(WAIT_TIME)  

print("\n***************************************************************" )
print("Get status of all lights.")
edge_server_1.get_status("LIGHT")
time.sleep(WAIT_TIME)

print("\n***************************************************************" )
print("Updating Ac_1 temperature to 18")
edge_server_1.set("ac_1","temperature",18)
time.sleep(WAIT_TIME)  


print("\n***************************************************************" )
print("Update switch status to ON for everything in Kitchen.")
edge_server_1.set("Kitchen",'switch_state','ON')
time.sleep(WAIT_TIME)

print("\n***************************************************************" )
print("Get status of all devices.")
edge_server_1.get_status("all")
time.sleep(WAIT_TIME)

print("\n***************************************************************" )
print("Get status of devices in kitchen.")
edge_server_1.get_status("Kitchen")
time.sleep(WAIT_TIME)

print("\n***************************************************************" )
print("Get status of devices in BR1.")
edge_server_1.get_status("BR1")
time.sleep(WAIT_TIME)

print("\n***************************************************************" )
print("Get status of all AC.")
edge_server_1.get_status("AC")
time.sleep(WAIT_TIME)

print("\n***************************************************************" )
print("Smart Home Simulation stopped.")
edge_server_1.terminate()
