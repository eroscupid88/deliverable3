#!/usr/bin/python3
import smbus2 as smbus
import math
import random
import re
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client
from cryptography.fernet import Fernet
import joystick as joyStick

"****************Broker IP address******************"
# raspberrypi 23 ip address from TAU LAB
publish_broker = '10.64.98.135'
# raspberrypi 32 ip address from TAU LAB
#subcribe_broker = '10.64.99.173'
#online broker1
#broker ='broker.emqx.io'
# online broker2
#broker = 'broker.hivemq.com'

"****************Initial variables******************"
port = 1883
topic_from_publisher = "RPI_command"
topic_from_subcriber = "RPI_command_sendover"
# generate client ID with pub prefix randomly
client_id = f'dtv782-subcribe-client-mqtt-{random.randint(1000, 2000)}'
from_publisher_command = 6
#username and password for rpi
username = 'pi'
password = 'raspberry'
msg =''

"****************Initial variables for rpi4******************"
lightPins = (12,13,16) #12: Green ; 13: Red ; 16: Blue
buttonPin = 11 # button pin
light_state = 0 # rpi4 states
parking_state = 0 # state to set up car parkign slot. 0 : no car is parking 1 : car is parking

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
address = 0x68       # This is the address value read via the i2cdetect command
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards



"****************Encryption******************"
#read encryption key from filekey.key file
with open('filekey.key','rb') as filekey:
    cipher_key = filekey.read().strip()
fernet = Fernet(cipher_key)

"****************MQTT Functions******************"

"""
connect_mqtt function : connect client to broker and return MQTT client type
"""
def connect_mqtt(broker) -> mqtt_client:
    def on_connect(client, userdata, flags, rc): #" print connection info"
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client 

"""
subcribe function take mqtt_client as a param, subcribe to broker and
decrypted and print out received message from that broker.
The messages also calculate time delay to send message from publisher and subscriber
    param: mqtt_client
    return: None
"""
def subscribe(client: mqtt_client):
    print(client)
    def on_message(client, userdata, msg):
        global from_publisher_command
        message = msg.payload.decode()
        print(f"Encrypted Message is : {message} \n\n")
        decrypted_message = fernet.decrypt(msg.payload).decode()
        machine = re.findall("^.{0,3}",decrypted_message)[0] #Find first 3 letters from message if it is `pub` the subcriber will receive  rpi4 command from publisher"
        publish_time =  float(re.findall("\d+\.\d+",decrypted_message)[0]) 
        current_time = time.time()
        delay_time =current_time - publish_time
        if machine == "pub":
            de_message = re.findall("[A-Z]+_[A-Z]+_[A-Z]+_[A-Z]+",decrypted_message)[0] #"Find command using regex"
            print(f"Decrypted Message is : {decrypted_message}\n\n ")
            print(f"Received message: {decrypted_message}\n\tTopic: {msg.topic}.\n\tPublish Machine time: {publish_time}\n\tSubcribe time: {current_time}\n\tDelay time:{delay_time}\n\tretaind flag: {msg.retain}")
            #client.unsubscribe(topic_from_publisher)
            if (de_message == "TURN_RED_LED_ON"):
                from_publisher_command = 0
            elif (de_message == "TURN_GREEN_LED_ON"):
                from_publisher_command = 1
            elif (de_message == "TURN_BLUE_LED_ON"):
                from_publisher_command = 2
            else:
                from_publisher_command = 3
            loop(client) #"call loop function and publish back to initial machine"
        else:
            print(f"Decrypted Message is : {decrypted_message}\n\n ")
            print(f"Received message: {decrypted_message}\n\tTopic: {msg.topic}.\n\tPublish Machine time: {publish_time}\n\tSubcribe time: {current_time}\n\tDelay time:{delay_time}\n\tretaind flag: {msg.retain}")
            loop(client) #"call loop function and publish back to initial machine"
    client.subscribe(topic_from_publisher)
    client.on_message = on_message

"""
publish function take 2 parameters mqtt_client and String: publish message receive from rpi4 as an encrypted message
under a topic to broker.
when publish, client can also set quality of service and change retain flag
param: client: mqtt_client type
       msg :string type
return: None
"""
def publish(client:mqtt_client,msg):
    encrypted_msg = fernet.encrypt(msg.encode())        
    result = client.publish(topic_from_publisher,encrypted_msg,qos=0,retain=False)
    status = result[0]
    if status ==0:
        print(f"send {encrypted_msg} to topic `{topic_from_publisher}`\n")
    else:
        print(f"Failed sent message\n")

"""
run function : main function to call connect client to broker, start loop
and subscribe client to broker
"""
def run():
    client = connect_mqtt(publish_broker)
    subscribe(client)
    client.loop_forever()


"****************RaspberryPi GPIO Functions******************"
"""
Initialize RaspberryPi GPIO function
"""
def setup():
    GPIO.setmode(GPIO.BOARD) # set BOARD mode
    GPIO.setup(lightPins,GPIO.OUT) # LED pin as output
    GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin as input pin pull up
    GPIO.add_event_detect(buttonPin,GPIO.BOTH, callback=pressButton,bouncetime = 100) # activate callback function when press button
    
"""
    blinkLinght function take 1 parameter (0 | 1) to change rpi4 state
    and also change LED colors
    pram: state: 0 | 1
    
"""
def blinkLight(state):
    global light_state
    global parking_state
    if ((state == 0 and light_state == 0)or (state == 0 and light_state == 4)):
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        light_state = 1
        print('light_state: %s'%light_state)
        return light_state
    if (state == 0 and light_state ==1):
        GPIO.output(12,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        light_state = 2
        print('light_state: %s'%light_state)
        return light_state
    if (state== 0 and light_state ==2):
        GPIO.output(16,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        light_state = 3
        print('light_state: %s'%light_state)
        return light_state
    if (state==0 and light_state == 3):
        GPIO.output(16,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        light_state = 4
        print('light_state: %s'%light_state)
        return light_state
    if (state==0 and light_state == 4):
        light_state = 0
        print('light_state: %s'%light_state)
        return light_state
    if (parking_state == 0):
        parking_state = 1
    else:
        parking_state = 0
    print(f"wtf: {parking_state}")
    return parking_state
"""
    pressButton callback function when button is pressed
    activate blinkLight function
"""
def pressButton(channel):
    print("button has been pressed")
    blinkLight(GPIO.input(buttonPin))




"********************calculation function for MPU6050 Gyro Acceleration Sensor"
def read_byte(adr):
    return bus.read_byte_data(address, adr)

#Read data and return value from address
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val
#Read data and return value from address
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

# Find position of P(a,b)
def dist(a,b):
    return math.sqrt((a*a)+(b*b))

#find y rotation
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
#find x rotation
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

"""
    loop function takee mqtt_client as parameter ,read data from sensor, publish message from rpi4 back to
    initial machine change its colour
    pram: client: mqtt_client type
"""
def loop(client:mqtt_client):
    bus.write_byte_data(address, power_mgmt_1, 0)
    #while(True):
    #pass
    global light_state
    global from_publisher_command
    global msg
    if from_publisher_command == 3:          
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)
        a ="gyro_xout : "+ str(gyro_xout)+ " scaled: "+ str((gyro_xout / 131))+"\n"
        b = "gyro_yout : "+ str(gyro_yout)+ " scaled: "+ str((gyro_yout / 131))+"\n"
        c="gyro_zout : "+ str(gyro_zout)+ " scaled: "+ str((gyro_zout / 131))+"\n"
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        d="accel_xout: "+ str(accel_xout)+ " scaled: "+ str(accel_xout_scaled)+"\n"
        e="accel_yout: "+ str(accel_yout)+ " scaled: "+ str(accel_yout_scaled)+"\n"
        f="accel_zout: "+ str(accel_zout)+ " scaled: "+ str(accel_zout_scaled)+"\n"
        g="x rotation: " + str(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))+"\n"
        h="y rotation: " + str(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))+"\n"

        msg = a+b+c+d+e+f+g+h + "with time: "+ str(time.time())
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12,GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        
        publish(client,msg)
    elif from_publisher_command == 0:
        msg = (f"RED light on with time: {time.time()}")
        light_state =0
        blinkLight(0)
        publish(client,msg)
    elif from_publisher_command == 1:
        msg = (f"GREEN light on with time: {time.time()}")
        light_state =1
        blinkLight(0)
        publish(client,msg)
    #else:
     #   msg = (f"BLUE light on with time: {time.time()}")
      #  light_state =2
       # blinkLight(0)
    time.sleep(2)
    
        
"""
    reset function destroy()
"""
def destroy():
    GPIO.output(lightPins,GPIO.HIGH)
    GPIO.cleanup()
   

if __name__ == "__main__":
    setup()
    try:
        run()
        #loop()
    except KeyboardInterrupt:
        destroy()
    
