from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import main_window_ui
from PyQt5.QtWidgets import QMessageBox
import request_client
import re


"""
    main class
"""
class MainWindow(QtWidgets.QMainWindow,main_window_ui.Ui_MainWindow):
    broker = '10.64.98.135'
    port = 1883
    name = 'publisher'
    topic = 'CME466-deliverable3'
    topic1 = 'another-topic'
    """
        constructor
    """
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
        

    
    def sendCommand(self):
        self.client.run_publish(self.topic1,"1")

    def receivedSignalFromRpi(self,message):
        print(message)


"""
    ,main function just running standalone
"""
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
