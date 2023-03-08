#!/urs/bin/python3
from paho.mqtt import client as mqtt_client
import random
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject
"""
    mqtt client class
"""
class MqttClient(QThread):
    messageReceived =pyqtSignal(str)

    """
        construction
    """
    def __init__(self,broker,port,topic,name,parent=None):
        super().__init__(parent)
        self.broker =broker
        self.port = port
        self.topic =topic
        self.client_id = f'dtv782-{name}-client-mqtt-{random.randint(1000,2000)}'
        self.client = self.connect_mqtt()
       

    """
        connect mqtt function connect client with broker and return the client
        prams: None
        return: mqtt_client type
    """
    def connect_mqtt(self):
        def on_connect(client,userdata,flags,rc):
            print(f"connect {client}, {userdata} , {flags}, {rc}")
            if rc == 0:
                print("Connect to MQTT broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker,self.port)
        return client

    """
        subscribe function take mqtt_client as parameter, subscribe topic and output message to terminal
        prams:
            client: mqtt_client type

        return: None
    """
    def subscribe(self,client,topic):
        def on_message(client,userdata,msg):
            print(msg)
            self.messageReceived.emit(msg)
        client.subscribe(topic)
        client.on_message = on_message
        
    """
        publish function take mqtt_client and a string message as parameters, publish message to broker
    """
    def publish(self,client,topic,msg):
        
        if topic == self.topic:
            time.sleep(1)
            client.publish(topic,encrypted_msg)
            #print(f"[Sending Message from RPI with topic `{topic}`]: \n{msg}")

        else:
            #print(f"[Sending Message from GUI with topic `{topic}`] :\n")
            client.publish(topic,encrypted_msg)
            #print(f"Message to RPI is:{msg}")


    def run_publish(self,topic,msg):
        self.client.loop_start()
        self.publish(self.client,topic,msg)

    def run(self):
        self.client.loop_start()
        self.subscribe(self.client,self.topic)

    def disconnect(self):
        pass
if __name__ == '__main__':
    broker = '10.64.98.135'
    port = 1883
    name = 'subscribe'
    topic = 'CME466-deliverable3'
    client =MqttClient(broker,port,topic,name)
    try:
        client.run_publish(topic,"test")
    except KeyboardInterrupt:
        client.disconnect()





