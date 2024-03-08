import pigpio
import time
import numpy as np

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html
FRONT = [17, 23] # Left, Right
REAR = [10, 24] # Left, Right
SEPA_FIN = 11
SEPA_RIN = 16
PINS = FRONT + REAR + [SEPA_FIN, SEPA_RIN]

class Motor(object):
    def __init__(self):
        Motor.pi = pigpio.pi()
        self.max_dutycycle = 100
        for pin in PINS:
            Motor.pi.set_mode(pin, pigpio.OUTPUT)
            Motor.pi.set_PWM_frequency(pin, 10000)
            Motor.pi.set_PWM_range(pin, 100)
    
    def forward(self):
        [Motor.pi.set_PWM_dutycycle(pin, self.max_dutycycle) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("forward")
        
    def back(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in FRONT]
        [Motor.pi.set_PWM_dutycycle(pin, self.max_dutycycle) for pin in REAR]
        print("back")
    
    def stop(self):
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in PINS]
        print("stop")
        
    def turn_right(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], self.max_dutycycle * 0.7) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], self.max_dutycycle) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn right")
    
    def turn_left(self):
        Motor.pi.set_PWM_dutycycle(FRONT[0], self.max_dutycycle) # Left
        Motor.pi.set_PWM_dutycycle(FRONT[1], self.max_dutycycle * 0.7) # Right
        [Motor.pi.set_PWM_dutycycle(pin, 0) for pin in REAR]
        print("turn left")
        
    def separate(self):
        Motor.pi.set_PWM_dutycycle(SEPA_FIN, 50) 
        Motor.pi.set_PWM_dutycycle(SEPA_RIN, 0)
        print("parachute separated")
                
    def attach_para(self):
        Motor.pi.set_PWM_dutycycle(SEPA_FIN, 0) 
        Motor.pi.set_PWM_dutycycle(SEPA_RIN, 50) 
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
