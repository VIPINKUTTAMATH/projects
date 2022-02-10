import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

HOST = "localhost"
PORT = 1883


class Light_Device():

    # setting up the intensity choices for Smart Light Bulb  
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    def _register_device(self, device_id, room_type, device_type):
        request = {"type":"register", "flag":"SYN", "device_id": device_id, "room_type": room_type, "device_type":device_type }
        topic_name = "home"
        publish.single(topic=topic_name, payload=json.dumps(request), hostname=HOST)


    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        client.subscribe(self._device_id, 0)
        client.subscribe(self._device_type, 0)
        client.subscribe(self._room_type, 0)
        client.subscribe(self._room_type+"/"+self._device_type, 0)
        client.subscribe("all", 0)
        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        reqString = "Light Device - " + self._device_id + " : " + str(msg.payload)
        print(reqString)
        request = json.loads(msg.payload)
        
        if request['type'] == 'set':
            if request['flag'] == 'switch_state':
                self._set_switch_status(request['value'])
            if request['flag'] == 'light_intensity':
                self._set_light_intensity(request['value'])
            
            response = {"type":"set", "status": 0, "device_id": self._device_id}
            topic_name = "home"
            publish.single(topic=topic_name, payload=json.dumps(response), hostname=HOST)
                
        if request['type'] == 'status':
            self.get_status()

    # Getting the current switch status of devices 
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_status = switch_state

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        return self._light_intensity
        
    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        self._light_intensity = light_intensity
        
    def get_status(self):
        response = {"type":"status", "light_intensity":self._get_light_intensity(), "switch_status":self._get_switch_status() ,"device_id": self._device_id, "room_type": self._room_type, "device_type":self._device_type }
        topic_name = "home"
        publish.single(topic=topic_name, payload=json.dumps(response), hostname=HOST)
    
    def _on_disconnect(self, client, userdata, flags, result_code):
        print(self.device_id,"client disconnected")