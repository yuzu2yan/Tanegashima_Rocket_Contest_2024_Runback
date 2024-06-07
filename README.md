# Tanegashima_Rocket_Contest_2024_Runback
![release_date](https://img.shields.io/badge/release_date-May_2024-yellow)
[![python](https://img.shields.io/badge/python-v3.9.2-blue)](https://www.python.org/downloads/release/python-392/)
[![openCV](https://img.shields.io/badge/OpenCV-v4.7.0-blue)](https://docs.opencv.org/4.7.0/)
![linux11](https://img.shields.io/badge/os-linux11-blue)  
[![python](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)](https://www.python.org/)
[![linux](https://img.shields.io/badge/-Linux-6C6694.svg?logo=linux&style=flat)](https://www.linux.org/)
[![raspberrypi](https://img.shields.io/badge/-Raspberry%20Pi-C51A4A.svg?logo=raspberry-pi&style=flat)](https://www.raspberrypi.com/)

This is a project of Team Astrum, CanSat and Runback Division of Tanegashima Rocket Contest 2024. 

<img width="400px" alt="intro_img" src="https://github.com/yuzu2yan/Tanegashima_Rocket_Contest_2024_Runback/assets/89567103/f631ac84-81dd-41cf-8d86-e2352d85866c">

## Mission  
The drone is dropped from 30 m above the ground, decelerated by a parachute, and lands on the ground. The drone aims for a zero-distance goal to a pylon placed at the goal point under autonomous control.  
  
## Mission Sequence  
The program starts when the carrier is loaded, and judges the ascent and landing by the air pressure sensor. In case of a sensor error, the landing judgment is also made over time. After landing, the separation mechanism is activated, and the CanSat uses the geomagnetic sensor and GPS to reach the goal. After approaching the goal, the camera starts image processing and distance measurement, and the program terminates when it judges that the goal has been reached.

## Feature
### Impact resistance due to bearings

<img width="400" alt="bearing" src="https://github.com/yuzu2yan/Tanegashima_Rocket_Contest_2024_Runback/assets/89567103/3c9b37c9-6141-4e8a-b578-ee44be46fc68">

Bearings are mounted on the axles of the tires to absorb the shock of landing. In addition, rigidity is secured by using TPU for the tires and CFRP for the body.

### Real-time object detection

<img width="400" alt="cone_detection" src="https://raw.github.com/wiki/yuzu2yan/Tanegashima_Rocket_Contest_2024_Runback/images/detection.gif">

The TPU accelerator allows for 30 object detections per second and goal detection using the Tensorflow framework. 

### Distance measurement using ToF camera

<img width="400" alt="tof_camera" src="https://raw.github.com/wiki/yuzu2yan/Tanegashima_Rocket_Contest_2024_Runback/images/tof.gif">

The position of the detected object can be transferred to the image acquired by the ToF camera to measure the distance to that point.  This allows for an accurate 0-distance goal.

## Success Criteria  

| | Statement | Methodology |
| ---- | ---- |---|
| Minimum Success |- Parachute separation at 2m altitude <br> - Landing without damage|Confirmation by visual inspection and log|
| Full Success |Zero-distance goal|Confirmation by visual inspection and log|
| Extra Success |Mission accomplishment within 3 minutes|Timer and log|


## Software Configuration
Language : Python 3.9.2  
OS       : Raspberry Pi OS Lite (32-bit)   
Raspbian GNU/Linux 11 (bullseye)    
Kernel   : Ver.5.15    
OpenCV   : Ver.4.7.0   
Tensorflow: Ver.2.15.0

## Hardware Configuration

Computer                   : Raspberry pi4  
GPS                        : GYSFDMAXB  
9-axis sensor              : BNO055  
Barometric pressure sensor : BME280   
Vision Camera              : ELP 1080P Global Shutter USB Camera    
ToF Camera                 : Arducam ToF Camera  
TPU                        : Coral USB Accelerator  
Motor Driver               : BD6231F  


## Program Configuration

- main.py  
    Main program. Operates according to the flow of the mission sequence.
- logger.py  
    Define a log class. Create logs for each phase and error and output them in csv format.
- floating.py  
    Used to calculate altitude; obtains air pressure and temperature from the BME280 module and calculates the altitude relative to the initial altitude.
- ground.py  
    This program is used in the ground phase. It calculates the distance and angle to the goal based on geomagnetic and GPS information, and determines the control.
- bme280.py  
    Obtain air pressure and temperature data using BME280.
- gnss.py  
    Obtains latitude and longitude from a GPS module every second. The acquisition program runs as a daemon.
- bno055.py  
    Obtain barometric pressure and acceleration data from BNO055. Each value is automatically calibrated by the built-in microcomputer, and the degree of calibration can be checked.
- cone_detection.py  
    It is an image processing module that takes a picture and detects red pylons in real time from the image.
- tof_distance.py
      Measure the position and distance to the red cone using a ToF camera.
- motor.py  
    This class deals with motors, controlling tires and deployment motors.

## Result
It was retired due to a damaged circuit board before the drop.

<img width="400px" alt="result_img" src="https://github.com/yuzu2yan/Tanegashima_Rocket_Contest_2024_Runback/assets/89567103/8ef6777b-da15-459b-8ad7-a3177bff7803">

