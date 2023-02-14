from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import main_window_ui
from PyQt5.QtWidgets import QMessageBox
import request_client
import re

class MainWindow(QtWidgets.QMainWindow,main_window_ui.Ui_MainWindow):
    broker = '10.64.98.135'
    port = 1883
    name = 'publisher'
    topic = 'CME466-deliverable3'
    topic1 = 'another-topic'

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.light = 0
        self.warnOnButton.clicked.connect(self.sendWarnOnLight)
        self.warnOffButton.clicked.connect(self.sendWarnOffLight)
        self.messageButton.clicked.connect(self.sendCommand)
        self.dic = {0:self.parkingLot1,1:self.parkingLot2,2: self.parkingLot3,3:self.parkingLot4,4:self.parkingLot5}
        self.parkingLot = [0,0,0,0,0]
        self.client = request_client.MqttClient(self.broker,self.port,self.topic,self.topic1,self.name,None)
        self.client.messageReceived.connect(self.displaySensorData)

        self.client.start()
        


    def sendWarnOnLight(self):
        self.client.run_publish(self.topic1,1)
    def sendWarnOffLight(self):
        self.client.run_publish(self.topic1,0) 
    def setParkingLot(self,data):
        self.parkingLot = data

    def showParkingLot(self):
        for index,value in enumerate(self.parkingLot):
            self.dic[index].setChecked(value)
    
    def displaySensorData(self,message):
        messages = re.split("\n",message)
        print(messages[0])
        self.setParkingLot([int(i) for i in re.split(' ',messages[0])])
        sensor = '\n'.join(messages[1:len(messages)])
        self.displaySensorDataMessage.setText(sensor)
        self.showParkingLot()

    def sendCommand(self):
        message = self.message_to_displace.toPlainText()
        self.client.run_publish(self.topic1,message)
        self.message_to_displace.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
