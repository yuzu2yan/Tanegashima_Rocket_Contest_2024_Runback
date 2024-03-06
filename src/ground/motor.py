import pigpio
import time
import numpy as np

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html
FRONT = [10, 24] # Left, Right
REAR = [17, 23] # Left, Right
SEPA_FIN = 11
SEPA_RIN = 16
PINS = FRONT + REAR + [SEPA_FIN, SEPA_RIN]

class Motor(object):
    def __init__(self):
        Motor.pi = pigpio.pi()
        for pin in PINS:
            Motor.pi.set_mode(pin, pigpio.OUTPUT)
            Motor.pi.set_PWM_frequency(pin, 10000)
            Motor.pi.set_PWM_range(pin, 100)
    
    def forward(self):
        [Motor.pi.set_PWM_dutycycle(pin, 100) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("forward")
        
    def back(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, 100) for pin in REAR]
        print("back")
    
    def stop(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in PINS]
        print("stop")
        
    def turn_right(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], 70) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], 100) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn right")
    
    def turn_left(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], 100) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], 70) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn left")
        
    def separate(self):
        Motor.pi.set_PWM_dutycycle(SEPA_FIN, 100) 
        Motor.pi.set_PWM_dutycycle(SEPA_RIN, 0)
        print("parachute separated")
                
    def attach_para(self):
        Motor.pi.set_PWM_dutycycle(SEPA_FIN, 0) 
        Motor.pi.set_PWM_dutycycle(SEPA_RIN, 100) 
        print("parachute attached")
        

if __name__ == '__main__':
    drive = Motor()
    movement = {'w': drive.forward, 'a': drive.turn_left, 's': drive.back, 'd':drive.turn_right, 'q': drive.stop, 'sep': drive.separate, 'para': drive.attach_para}
    while True:
        c = input('Enter char : ')
        if c in movement.keys():
            movement[c]()
        elif c == 'z':
            break
        else:
            print('Invalid input')
