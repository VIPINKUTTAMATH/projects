
import json
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25  

class Edge_Server:
    
    def __init__(self, instance_name, callBack):
        
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []
        self.callBack = callBack

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        client.subscribe("home/#", 0)
        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        print("Edge server :" , msg.payload)
        response = json.loads(msg.payload)        
        if response['type'] == 'register':
            topic_name = response['device_id']
            response['flag']='ACK'
            self._registered_list.append(response['device_id'])
            publish.single(topic=topic_name, payload=json.dumps(response), hostname=HOST)
        
        if response['type'] == "set" and response['status'] == 0:
            topic_name = response['device_id']
            request = {"type": "status"}
            publish.single(topic=topic_name, payload=json.dumps(request), hostname=HOST)
            
        if response['type'] == "status":
            self.callBack(msg.payload)
            
    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self,topic_name):
        request = {"type": "status"}
        publish.single(topic=topic_name, payload=json.dumps(request), hostname=HOST)

    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self, topic_name, command, value):
        request = {"type": "set", "flag":command, "value":value }
        publish.single(topic=topic_name, payload=json.dumps(request), hostname=HOST)
        