#!urs/bin/python3
import time
from picamera import PiCamera
from datetime import datetime
import request_client


"""
    rpi4 class
"""
class Rpi4(object):
    """
        variables
    """
    broker ='10.64.98.135'
    port = 1883
    name = 'publish'
    topic = 'CME466-exam'
    topic1 ='from GUI'

    """
        constructor
    """
    def __init__(self):
        super().__init__()
        self.mqttClient = request_client.MqttClient(self.broker,self.port,self.topic,self.topic1,self.name)
        self.camera = PiCamera()
        self.setup()
        self.takePicture()
        self.received = True
        
        
    def setup(self):
        self.camera.resolution= (1280,720)
    def active(self):
        self.received = True
    def takePicture(self):
        now = datetime.now()
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        self.camera.start_preview()
        self.camera.annotate_text = f"Dillon Vu \n {dt_string}"
        time.sleep(5)
        self.camera.capture('./exam.jpg')
        self.camera.stop_preview()
        print(dt_string)
    def response(self):
        return "Photo taken and saved!"
    def receiveCommand(self):
        return self.received
    def loop_with_mqtt(self):
        while True:
            # data = ' '.join(str(i) for i in self.parking_data) +"\n"+ sensor.toString()
            # if (self.response):
            self.mqttClient.subscribe(self.mqttClient.client,self.topic1)
            if (self.mqttClient.message_to_rpi == '1'):
                self.received = True
                self.takePicture()
                self.mqttClient.run_publish(self.topic,self.response())
            
            # self.run_display()

    """
        destroy function reset lightPins to HIGH
    """
    def destroy(self):
        pass

if __name__ == '__main__':
    rpi = Rpi4()
    try:
        rpi.loop_with_mqtt()
    except KeyboardInterrupt:
        rpi.destroy()
