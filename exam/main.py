from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import window_ui
from PyQt5.QtWidgets import QMessageBox
import request_client
import re


"""
    main class
"""
class MainWindow(QtWidgets.QMainWindow,window_ui.Ui_MainWindow):
    broker = '10.64.98.135'
    port = 1883
    name = 'publisher'
    topic = 'CME466-exam'
    topic1 ='from GUI'
    """
        constructor
    """
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.sendCommand)
        self.client = request_client.MqttClient(self.broker,self.port,self.topic,self.topic1,self.name,None)
        self.client.messageReceived.connect(self.receivedSignalFromRpi)

        self.client.start()
        

    
    def sendCommand(self):
        self.client.run_publish(self.topic1,"1")
        print("something")

    def receivedSignalFromRpi(self,message):
        print(message)
        self.textEdit.setText(message)


"""
    ,main function just running standalone
"""
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
