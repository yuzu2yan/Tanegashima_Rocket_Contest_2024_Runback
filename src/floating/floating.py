import sys
sys.path.append('./../sensors')
sys.path.append('./../ground')
from sensors import bme280
from ground import motor
import time

SEA_LEVEL_PRESSURE = 1013.25

def cal_altitude(init_altitude):
    data = bme280.read_BaroData()
    """
    data[0] = pressure
    data[1] = temperature
    data[2] = altitude
    
    https://keisan.casio.jp/exec/system/1257609530
    altitude = (Sea level pressure / Current pressure)**(1 / 5.257) - 1) * (Current temperature + 273.15) / 0.0065
    """
    data[2] = ((SEA_LEVEL_PRESSURE / data[0])**(1 / 5.257) - 1) * (data[1] + 273.15) / 0.0065 - init_altitude
    return data

if __name__ == '__main__':
    drive = motor.Motor()
    state = 'Rising'
    data = cal_altitude(0)
    init_altitude = data[2]
    print("init_altitude : ", init_altitude)
    while state != 'Landing':
        """
        state Rising
              Ascent Completed
              Landing
              Error
        """
        while state == 'Rising':
            data = cal_altitude(init_altitude)
            altitude = data[2]
            print("Rising")
            if altitude >= 5:
                state = 'Ascent Completed'
            time.sleep(1)
        while state == 'Ascent Completed':
            data = cal_altitude(init_altitude)
            altitude = data[2]
            print("Ascent Completed")
            if altitude <= 3:
                state = 'Landing'
            time.sleep(0.1)
        drive.servo() # Separation mechanism activated