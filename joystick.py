#!/usr/bin/env python3
import PCF8591 as ADC 
import time
from enum import Enum

class ParkingSlot(Enum):
    SLOT1 = 0
    SLOT2 = 1
    SLOT3 = 2
    SLOT4 = 3
    SLOT5 = 4

class JoyStick(object):
    """
        Constructor of JoyStick Object
    """
    def __init__(self):
        super().__init__()
        self.data = [0,0,0,0,0]
        self.mode = 0
        self.status = ''
        self.ADC =  ADC

        #calling function
        self.setup()
    """
        setup function set up ADC with choosen address
    """
    def setup(self):
	    self.ADC.setup(0x48)

    def setMode(self):
        if self.mode == 0:
            self.mode = 1
        else:
            self.mode = 0

    def setParking(self,index):
        if self.mode == 1:
            self.data[index] = 1
        else:
            self.data[index] = 0
    def getMode(self):
        return self.mode
    
    def getData(self):
        return self.data

    """
        direction function return a direction as string
        prams: None
        Return: a String type
    """
    def direction(self):
        print(f"0:{self.ADC.read(0)}\n 1:{self.ADC.read(1)}\n2: {self.ADC.read(2)}")
        state = ['home','parkingSlot1','parkingSlot2','parkingSlot3','parkingSlot4','pressed', 'parkingSlot5']
        i = 0
        if (self.ADC.read(1) == 255 and self.ADC.read(2) == 128):

            i = 0
        if (self.ADC.read(2) == 0 or self.ADC.read(2) == 1):
            self.setMode()
            i = 5
        if (self.ADC.read(1) > 126 and self.ADC.read(1) < 254 ):
            self.setParking(ParkingSlot.SLOT1.value)
            i = 1
        if (self.ADC.read(0) >= 22 and self.ADC.read(0) <=27):
            self.setParking(ParkingSlot.SLOT2.value)
            i = 2
        if (self.ADC.read(1) == 255):
            self.setParking(ParkingSlot.SLOT3.value)
            i = 3
        if (self.ADC.read(1) ==0):
            self.setParking(ParkingSlot.SLOT4.value)
            i = 4
        if (self.ADC.read(0) > 4 and self.ADC.read(0) <= 22):
            self.setParking(ParkingSlot.SLOT5.value)
            i = 6
        return state[i]

    """
        while loop function running constaintly to print out the direction of the joinstick
    """
    def loop(self):
        status = ''
        while True:
            print(f"status is {status}")
            tmp = self.direction()
            if tmp != None and tmp != status:
                print(tmp)
                status = tmp
            time.sleep(1)
            print(f"mode is: {self.mode}")
            
    def destroy(self):
        pass

"""
    main function call when running joinstick independently
"""
if __name__ == '__main__':
    joyStick = JoyStick()
    try:
        joyStick.loop()
    except KeyboardInterrupt:
        joyStick.destroy()


