#!/urs/bin/python3
import smbus2 as smbus
import math
import time

class Sensor_Mpu6050():

    def __init__(self):
        super().__init__()
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1)
        self.address = 0x68
        self.gyro_x_adr = 0x43
        self.gyro_y_adr = 0x45
        self.gyro_z_adr = 0x47
        self.accel_x_adr =0x3b
        self.accel_y_adr = 0x3d
        self.accel_z_adr = 0x3f
        self.bus.write_byte_data(self.address,self.power_mgmt_1,0)

    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address,adr)

    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address,adr)
        low  = self.bus.read_byte_data(self.address,adr+1)
        val = (high << 8) + low
        return val
    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if(val >=0x8000):
            return -((65535 -val) + 1)
        else:
            return val
    def dist(self,a,b):
        return math.sqrt((a*a+b*b))

    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x,dist(y,z))
        return -math.degrees(radians)
    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y,dist(x,z))
        return math.degrees(radians)
    
    def get_gyro_scale(self,gyro_out):
        return gyro_out/131


    def toString(self):
        aString = ''
        gyro_xout = self.read_word_2c(self.gyro_x_adr)
        
        gyro_yout = self.read_word_2c(self.gyro_y_adr)
        
        gyro_zout = self.read_word_2c(self.gyro_z_adr)
        

        return aString + "gyro_xout : " + str(gyro_xout) + " scaled: " + str(self.get_gyro_scale(gyro_xout))+"\ngyro_yout : " +str(gyro_yout) + " scaled: "+str(self.get_gyro_scale(gyro_yout)) + "\ngryo_zout : " +str(gyro_zout) + " scaled " + str(self.get_gyro_scale(gyro_zout))+"\n"


    def loop(self):
        while True:
            time.sleep(1)
            print(self.toString())
            time.sleep(1)
    def destroy():
        pass

if __name__ == '__main__':
    sensor = Sensor_Mpu6050()
    try:
        sensor.loop()
    except KeyboardInterrupt:
        sensor.destroy()
