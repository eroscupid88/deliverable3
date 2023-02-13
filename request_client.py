#!/urs/bin/python3
from paho.mqtt import client as mqtt_client
import random
import rpi4
import joystick
import sensor_MPU6050
import encryption
import time
import main
from PyQt5.QtCore import QThread, pyptSignal

class MqttClient(object):
    messageReceived =pyqtSignal(str)

    """
        construction
    """
    def __init__(self,broker,port,topic,name,rpi):
        self.encryption = encryption.EncryptionObject('filekey.key')
        self.broker =broker
        self.port = port
        self.topic =topic
        self.light_command = 0
        self.received_message = ''
        self.topic1 ="ho"
        self.client_id = f'dtv782-{name}-client-mqtt-{random.randint(1000,2000)}'
        self.rpi = None
        self.client = self.connect_mqtt()
        if rpi == None:
            pass
        else:
            self.rpi = rpi
        print(self.rpi)
       

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
    def subscribe(self,client,rpi):
        def on_message(client,userdata,msg):
            message = msg.payload.decode()
            print(f"[Received Message from RPI]: \n{message}")
            self.messageReceived.emit(message)

            self.publish(self.client,self.rpi)
        def on_message_response(client,userdata,msg):
            message = msg.payload.decode()
            print(f"[Received Message from GUI]: \n{message}")

        if rpi== None:
            client.subscribe(self.topic)
            client.on_message = on_message
        else:
            client.subscribe(self.topic1)
            client.on_message = on_message_response

    """
        publish function take mqtt_client and a string message as parameters, publish message to broker
    """
    def publish(self,client,rpi,msg):
        if rpi != None:
            time.sleep(1)
            rpi.sendData()
            msg_array = rpi.parking_data
            msg = ' '.join(str(i) for i in msg_array)
            msg = msg + '\n' + rpi.sensor.toString()
            client.publish(self.topic,msg)
            print(f"[Sending Message from RPI]: \n{msg}")

        else:
            print(f"[Sending Message from GUI] :\n")
            client.publish(self.topic1,msg)


    def run_publish(self,msg):
        self.client.loop_start()
        self.publish(self.client,self.rpi,msg)
        self.subscribe(self.client,self.rpi)
        self.client.loop_forever()

    def run_subscribe(self):
        #self.client.loop_start()
        self.subscribe(self.client,self.rpi,callback)
        self.client.loop_forever()

    def disconnect(self):
        pass
if __name__ == '__main__':
    broker = '10.64.98.135'
    port = 1883
    name = 'subscribe'
    topic = 'CME466-deliverable3'
    joystick = joystick.JoyStick()
    sensor = sensor_MPU6050.Sensor_Mpu6050()
    #app  = main.QtWidgets.QApplication(main.sys.argv)
    #mainWindow = main.MainWindow()
    #mainWindow.show()
    rpi = rpi4.Rpi4(sensor,joystick)
    client =MqttClient(broker,port,topic,name,rpi)
    try:
        client.run_publish()
    except KeyboardInterrupt:
        client.disconnect()





