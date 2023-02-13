import paho.mqtt.client as mqtt_client
import random
import time
import os.path
import re
from cryptography.fernet import Fernet

class MQTT_Client(object):
    def __init__(self):
        "****************Broker IP address******************"
        # raspberry pi 23 ip address from TAU LAB
        self.publish_broker = '10.64.98.135'
        # raspberry pi 32 ip address from TAU LAB
        #subcribe_broker = '10.64.99.173'
        # online broker1
        #publish_broker = 'broker.emqx.io'
        # online broker2
        #publish_broker = 'broker.hivemq.com'
        "****************Initial variables******************"
        self.port =1883
        self.topic_from_publisher = "RPI_command"
        self.topic_from_subcriber = "RPI_command_sendover"
        self.username = 'pi'
        self.password = 'raspberry'
        self.client_id = f'dtv782-publish-mqtt-{random.randint(0,1000)}'
        self.cipher_key = ''

        "****************Encryption******************"
        #check if there is filekey.key. If not generate new key and save it to file
        if not os.path.isfile('./filekey.key'):
            self.cipher_key =  Fernet.generate_key()
            with open('filekey.key','wb') as filekey:
                filekey.write(self.cipher_key)
        else:
            with open('filekey.key','rb') as filekey:
                self.cipher_key = filekey.read().strip()
        self.cipher = Fernet(self.cipher_key)


    "****************MQTT Functions******************"

    """
    connect_mqtt function : connect client to broker and return MQTT client type
    """
    def connect_mqtt(self,broker):
        client =mqtt_client.Client(self.client_id)
        def on_connect(client,userdata,flags,rc):
            if rc == 0:
                client.connect_flag=True
                print("Connect to MQTT Broker!!")
            else:
                client.bad_connection_flag=True
                print("fail to connect, return code %d\n",rc)
                if (rc== 5):
                    print("required more infomation")
        client.username_pw_set(self.username,self.password)
        client.on_connect = on_connect
        client.connect(broker,self.port)
        return client

    """
    publish function take 1 parameter mqtt_client : publish encrypted commands message 
    under a topic to broker.
    when publish, client can also set quality of service and change retain flag
    param: client: mqtt_client type

    return: None
    """
    def publish(self,client):
        command = ["TURN_RED_LED_ON", "TURN_GREEN_LED_ON","TURN_BLUE_LED_ON","TURN_ACCEPT_SENSOR_DATA"]
        message = ''
        prompt_input = input(f"Choose Number for RPI Command here: \n1: {command[0]}\n2: {command[1]}\n3: {command[2]}\n4: {command[3]}\ninput:\t")
        if prompt_input == "1":
            message = command[0]
        elif prompt_input == "2":
            message = command[1]
        elif prompt_input == "3":
            message = command[2]
        else:
            message = command[3]  
        time.sleep(1)
        msg =f"pub: {message} with time: {time.time()} "
        encrypted_msg = self.cipher.encrypt(msg.encode())        
        result = client.publish(self.topic_from_publisher,encrypted_msg,qos=0,retain=False)
        status = result[0]
        if status ==0:
            print(f"send {encrypted_msg} to topic `{self.topic_from_publisher}`\n")
        else:
            print(f"Failed sent message\n")

    """
    subcribe function take mqtt_client as a param, subcribe to broker and
    decrypted and print out received messages from that broker which are data from rpi4.
        param: mqtt_client
        return: None
    """
    def subscribe(self,client: mqtt_client):
        print(client)
        def on_message(client, userdata, msg):
            message = msg.payload.decode()
            decrypted_message = self.cipher.decrypt(msg.payload).decode()
            
            machine = re.findall("^.{0,3}",decrypted_message)[0]
            if machine != "pub":
                print(f"Encrypted Message is : {message} \n\n")
                print(f"Received message: {decrypted_message}\n")
                
        client.subscribe(self.topic_from_publisher)
        client.on_message = on_message
    
    """
    run function : main function to call connect client to broker, start loop
    publish and subscribe client to broker
    """
    def run(self):
        client = self.connect_mqtt(self.publish_broker)
        time.sleep(1)
        self.publish(client)
        self.subscribe(client)
        client.loop_forever()

# if __name__ == '__main__':
#     mqtt_clients = MQTT_Client()
#     mqtt_clients.run()



