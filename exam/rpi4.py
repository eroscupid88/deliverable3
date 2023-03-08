#!urs/bin/python3
import time
from picamera import PiCamera
from datetime import date


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

    """
        constructor
    """
    def __init__(self):
        super().__init__()
        # self.mqttClient = request_client.MqttClient(self.broker,self.port,self.topic,self.name)
        self.camera = PiCamera()
        self.setup()
        self.takePicture()
        
        
    def setup(self):
        self.camera.resolution= (1280,720)

    def takePicture(self):
        today = date.today()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        camera.start_preview()
        self.camera.annotate_text = f"Dillon Vu \n {d1}"
        time.sleep(5)
        self.camera.capture('./exam.jpg')
        self.camera.stop_preview()
        
    def loop_with_mqtt(self):
        while True:
            pass
            # data = ' '.join(str(i) for i in self.parking_data) +"\n"+ sensor.toString()
            # self.mqttClient.run_publish(self.topic,data)
            # self.mqttClient.subscribe(self.mqttClient.client,self.topic1)
            # if (self.mqttClient.message_to_rpi.isdigit()):
            #     self.setWarningLight(int(self.mqttClient.message_to_rpi))
            # else:
            #     self.setBoardMessage(self.mqttClient.message_to_rpi)

            # self.run_display()

    """
        destroy function reset lightPins to HIGH
    """
    def destroy(self):
        pass

if __name__ == '__main__':
    rpi = Rpi4()
    # try:
    #     rpi.loop_with_mqtt()
    # except KeyboardInterrupt:
    #     rpi.destroy()