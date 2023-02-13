from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import main_window_ui
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow,main_window_ui.Ui_MainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.warnOnButton.clicked.connect(self.sendWarnOnLight)
        self.warnOffButton.clicked.connect(self.sendWarnOffLight)
        self.messageButton.clicked.connect(self.sendCommand)

    def sendWarnOnLight(self):
        print("send warn on light!!!")
    
    def sendWarnOffLight(self):
        print("send warn off light!!!")

    def sendCommand(self):
        print("send command to rpi4")
        self.displaySensorDataMessage.setText("Hello World")
        self.parkingLot1.setChecked(True)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())