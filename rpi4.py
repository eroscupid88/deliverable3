#!urs/bin/python3
import sensor_MPU6050
import joystick
import time
import encryption
import RPi.GPIO as GPIO
from enum import Enum
import request_client

class State(Enum):
    PARKING_CONTROL = 1
    READING_SENSOR = 2
    DISPLAY = 3


class Rpi4(object):
    broker ='10.64.98.135'
    port = 1883
    name = 'publish'
    topic = 'CME466-deliverable3'
    topic1 = 'another-topic'

    def __init__(self,sensor,joystick):
        super().__init__()
        self.mqttClient = request_client.MqttClient(self.broker,self.port,self.topic,self.topic1,self.name)
        self.state = State.DISPLAY 
        self.sensor = sensor
        self.joystick = joystick
        self.board_message = ''
        self.sensor_data = ''
        self.warning_light = 0
        self.parking_data = [0,0,0,0,0]    
        #initial variables fro GPIO
        self.lightPins = (12,13,16)
        print("initial set up RPI4")
        print(self.state.value)

        # initialize setup
        self.setup()

    def setup(self):
        print("************RPI4 is setting up**************\n")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.lightPins,GPIO.OUT)
        GPIO.output(self.lightPins[0],GPIO.HIGH)
        GPIO.output(self.lightPins[1],GPIO.HIGH) 
        GPIO.output(self.lightPins[2],GPIO.HIGH)

    def setWarningLight(self,mode):
        print("called")
        self.warning_light = mode
    def displayLight(self):
        print(self.warning_light)
        if (self.warning_light == 1):
            time.sleep(0.3)
            GPIO.output(self.lightPins[1],GPIO.LOW)
            time.sleep(0.3)
            GPIO.output(self.lightPins[1],GPIO.HIGH)
        else:
            GPIO.output(self.lightPins[1],GPIO.HIGH)
    def setBoardMessage(self,message):
        self.board_message = message
    def displayBoard(self):
        print(f"[Display Board] : {self.board_message} \n")
    def setParkingData(self,parking_data):
        self.parking_data = parking_data

    def run_display(self):
        self.displayLight()
        self.displayBoard()

    def loop_with_mqtt(self):
        while True:
            self.joystick.direction()
            self.setParkingData(joystick.getData())
            data = ' '.join(str(i) for i in self.parking_data) +"\n"+ sensor.toString()
            self.mqttClient.run_publish(self.topic,data)
            self.mqttClient.subscribe(self.mqttClient.client,self.topic1)
            if (self.mqttClient.message_to_rpi.isdigit()):
                self.setWarningLight(int(self.mqttClient.message_to_rpi))
            else:
                self.setBoardMessage(self.mqttClient.message_to_rpi)

            self.run_display()


    def destroy(self):
        GPIO.output(self.lightPins,GPIO.HIGH)

if __name__ == '__main__':
    sensor = sensor_MPU6050.Sensor_Mpu6050()
    joystick = joystick.JoyStick()
    rpi = Rpi4(sensor,joystick)
    try:
        rpi.loop_with_mqtt()
    except KeyboardInterrupt:
        rpi.destroy()
