"""""""""""""""""""""""""""""""""""
    TANEGASHIMA ROCKET CONTEST 2024
    ASTRUM RUNBACK MAIN PROGRAM
    
    Author : Yuzu
    Language : Python Ver.3.9.2
    Last Update : 03/01/2024
"""""""""""""""""""""""""""""""""""


import GYSFDMAXB
import motor
import ground
import floating
import img_proc
import logger
import time
import datetime
import csv
import yaml


print("Hello World!!")
error_log = logger.ErrorLogger()
drive = motor.Motor()
drive.stop()
# destination point(lon, lat)
with open('settings.yaml') as yml:
    settings = yaml.safe_load(yml)
des = [settings['destination']['longitude'], settings['destination']['latitude']]

"""
phase 1 : Floating
      2 : Ground 
      3 : Image Processing
      4 : Reach the goal
"""


"""
Floating Phase
"""
phase = 1
if phase == 1:
    print("phase : ", phase)
    floating_log = logger.FloatingLogger()
    """
    state 
        Rising
        Falling
        Landing
        Error
    """
    state = 'Rising'
    floating_log.state = 'Rising'
    start = time.time()
    # The flag that identifies abnormalities in the barometric pressure sensor
    error_baro = 0
    init_altitude = 0
    data = floating.cal_altitude(init_altitude)
    init_altitude = data[2]
    altitude = init_altitude
    print("initial altitude : {}." .format(init_altitude))
    floating_log.floating_logger(data)
    print("Rising phase")
while phase == 1:
    while state == 'Rising':
        data = floating.cal_altitude(init_altitude)
        pre_altitude = altitude
        altitude = data[2]
        floating_log.floating_logger(data)
        print("Rising")
        # Incorrect sensor value
        if altitude < -5:
            error_baro += 1
            if error_baro >= 15:
                state = 'Error'
                floating_log.state = 'Error'
                error_log.baro_error_logger(phase, data)
                print("Error : Altitude value decreases during ascent")
            time.sleep(1.5)
            continue
        if altitude >= 25:
            state = 'Ascent Completed'
            floating_log.state = 'Ascent Completed'
        now = time.time()
        if now - start > 480:
            print('8 minutes passed')
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase('Landing judgment by passage of time.')
            break
        print("altitude : {}." .format(altitude))
        time.sleep(1.5)
    while state == 'Ascent Completed':
        data = floating.cal_altitude(init_altitude)
        pre_altitude = altitude
        altitude = data[2]
        floating_log.floating_logger(data)
        print("Falling")
        if altitude <= 4:
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase()
        now = time.time()
        if now - start > 480:
            print('8 minutes passed')
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase('Landing judgment by passage of time.')
            break
        print("altitude : {}." .format(altitude))
        time.sleep(0.2)
    while state == 'Error':
        data = floating.cal_altitude(init_altitude)
        altitude = data[2]
        floating_log.floating_logger(data)
        now = time.time()
        if now - start > 480:
            print('8 minutes passed')
            state = 'Landing'
            floating_log.state = 'Landing'
            floating_log.end_of_floating_phase('Landing judgment by passage of time.')
            break
        time.sleep(1)
    print("Landing")
    drive.servo() # Separation mechanism activated
    break


drive.forward()
time.sleep(5)
drive.stop()
reach_goal = False
# The flag that identifies abnormalities in the image processing
error_img_proc = False
# Variable used for stack determination and GPS direction determination
pre_gps = [0,0]
phase = 2
# The flag indicating if the camera is deployed
ground_log = logger.GroundLogger()
ground_log.state = 'Normal'
img_proc_log = logger.ImgProcLogger()

while not reach_goal:
    """
    Ground Phase
    """
    print("phase : ", phase)
    while GYSFDMAXB.read_GPSData() == [0,0]:
            print("Waiting for GPS reception")
            time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    data = ground.is_heading_goal(gps, des)
    distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
    print("distance : ", distance)
    ground_log.ground_logger(data, distance)
    while phase == 2:
        # Goal judgment
        if distance <= 8 and error_img_proc == False: # Reach the goal within 8m
            print("Close to the goal")
            drive.stop()
            ground_log.end_of_ground_phase()
            phase = 3
            break
        # if distance <= 1 and error_img_proc: # Reach the goal without image processing
        #     print("Reach the goal")
        #     phase = 4
        #     ground_log.end_of_ground_phase('Reach the goal without image processing')
        #     drive.forward()
        #     time.sleep(2.0)
        #     drive.stop()
        #     break
        while data[3] != True: # Not heading the goal
            # Check the stack and position when there are many position adjustments
            if count % 5 == 0:
                stuck, diff_distance = ground.is_stuck(pre_gps, gps, data[13])
                print("accel : ", data[13])
                # Move away from the goal
                if distance - pre_distance > 0.22:
                    ground_log.state = 'Something Wrong'
                    error_log.heading_error_logger(phase, pre_gps, gps, pre_distance, distance)
                    print('Error : Heading direction is wrong')
                    drive.turn_right()
                    time.sleep(5)
                    drive.stop()
                    pre_gps = gps
                    gps = GYSFDMAXB.read_GPSData()
                    distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
                    print("distance : ", distance)
                    diff_distance = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
                    data = ground.is_heading_goal(gps, des, pre_gps)
                    ground_log.state = 'Normal' 
                    print('Finish Error Processing')
            if data[4] == 'Turn Right':
                drive.turn_right()
            elif data[4] == 'Turn Left':
                drive.turn_left()
            time.sleep(0.3)
            # The Value used for direction calculation with only position information
            pre_gps = gps
            gps = GYSFDMAXB.read_GPSData()
            # The value used to check if the rover is heading towards the goal
            pre_distance = distance
            distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
            print("distance : ", distance)
            # displacement from previous position
            diff_distance = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
            data = ground.is_heading_goal(gps, des, pre_gps)
            ground_log.ground_logger(data, distance, pre_gps, diff_distance)
        # End of Orientation Correction
        # Goal judgment again
        if distance <= 8 and error_img_proc == False: # Reach the goal within 8m
            print("Close to the goal")
            drive.stop()
            ground_log.end_of_ground_phase()
            phase = 3
            break
        if distance <= 1 and error_img_proc: # Reach the goal without image processing
            print("Reach the goal")
            phase = 4
            reach_goal = True
            ground_log.end_of_ground_phase('Reach the goal without image processing')
            drive.forward()
            time.sleep(2.0)
            drive.stop()
            break
        # Move towards the goal for 3 seconds
        drive.forward()
        time.sleep(3)
        pre_gps = gps
        gps = GYSFDMAXB.read_GPSData()
        data = ground.is_heading_goal(gps, des, pre_gps)
        pre_distance = distance
        distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
        print("distance : ", distance)
        diff_distance = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
        ground_log.ground_logger(data, distance, pre_gps, diff_distance)
        # Check the stack and position
        stuck, diff_distance = ground.is_stuck(pre_gps, gps, data[13])
        print("accel : ", data[13])
        # # Move away from the goal
        # elif distance - pre_distance > 0.22:
        #     ground_log.state = 'Something Wrong'
        #     error_log.heading_error_logger(phase, pre_gps, gps, pre_distance, distance)
        #     print('Error : Heading direction is wrong')
        #     drive.turn_right()
        #     time.sleep(5)
        #     drive.stop()
        #     pre_gps = gps
        #     gps = GYSFDMAXB.read_GPSData()
        #     distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
        #     print("distance : ", distance)
        #     diff_distance = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
        #     data = ground.is_heading_goal(gps, des, pre_gps)
        #     ground_log.state = 'Normal' 
        #     print('Finish Error Processing')
            
            
    """
    Image Processing Phase
    """
    print("phase : ", phase)
    p = 0
    not_found = 0
    while phase == 3 and error_img_proc == False:
        img_name = img_proc.take_picture()
        if img_name is not None:
            try:
                pre_p = p
                cone_loc, proc_img_name, p = img_proc.detect_cone(img_name)
                print("percentage of cone in img : ", p)
            except Exception as e:
                print("Error : Image processing failed")
                error_img_proc = True
                phase = 2
                error_log.img_proc_error_logger(phase, distance=0)
                with open('sys_error.csv', 'a') as f:
                    now = datetime.datetime.now()
                    writer = csv.writer(f)
                    writer.writerow([now.strftime('%H:%M:%S'), 'Image processing failed', str(e)])
                    f.close()
                drive.stop()
                break
        else:
            error_img_proc = True
            phase = 2
            print("Error : Failed to take a picture")
            error_log.img_proc_error_logger(phase, distance=0)
            drive.stop()
            break
        pre_gps = gps
        gps = GYSFDMAXB.read_GPSData()
        distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
        print("distance :", distance)
        diff_distance = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
        img_proc_log.img_proc_logger(img_name, proc_img_name, cone_loc, p, distance, gps, pre_gps, diff_distance)
        # Goal judgment(Supports too close to the goal)
        if p > 0.12 or (pre_p - p >= 0.02 and cone_loc != "Not Found"):
            print("Reach the goal")
            phase = 4
            reach_goal = True
            img_proc_log.end_of_img_proc_phase()
            drive.forward()
            time.sleep(2.0)
            drive.stop()
            break
        # The rover is far from the goal
        if distance >= 15:
            print('Error : The rover is far from the goal')
            error_log.far_error_logger(phase, gps, distance)
            drive.stop()
            drive.turn_right()
            time.sleep(5)
            drive.stop()
        if cone_loc == "Front":
            drive.forward()
        elif cone_loc == "Right":
            drive.turn_right()
            time.sleep(1.5) if p < 0.01 else time.sleep(1)
            drive.forward()
        elif cone_loc == "Left":
            drive.turn_left()
            time.sleep(1.5) if p < 0.01 else time.sleep(1)
            drive.forward()
        else: # Not Found
            not_found += 1
            if not_found >= 8:
                print('Error : Cone not found')
                # when GPS is enabled
                if error_heading < ERROR_HEADING:
                    # when the geomagnetic sensor is enabled
                    if error_mag == False:
                        gps = GYSFDMAXB.read_GPSData()
                        data = ground.is_heading_goal(gps, des, pre_gps, error_mag)
                        error_log.not_found_error_logger(phase, img_name, proc_img_name, p, not_found, data, pre_gps, error_mag, error_heading)
                        count = 0
                        while data[3] != True: # Not heading the goal
                            count += 1
                            if count % 5 == 0:
                                stuck, diff_distance = ground.is_stuck(pre_gps, gps, data[13])
                                # Stuck Processing
                                if stuck:
                                    img_proc_log.img_proc_logger(img_name, proc_img_name, cone_loc, p, distance, gps, pre_gps, diff_distance, 'Stuck judgment because the value of acceleration is {}m/s^2'.format(data[13]))
                                    print('stuck')
                                    drive.stuck()
                                    pre_gps = gps
                                    gps = GYSFDMAXB.read_GPSData()
                                    distance = ground.cal_distance(gps[0], gps[1], des[0], des[1])
                                    diff_distance = ground.cal_distance(pre_gps[0], pre_gps[1], gps[0], gps[1])
                                    continue
                            if count >= 30:
                                print("Error : Can't get out of stack")
                                break
                            if data[4] == 'Turn Right':
                                drive.turn_right()
                            elif data[4] == 'Turn Left':
                                drive.turn_left()
                            time.sleep(0.3)
                            pre_gps = gps
                            gps = GYSFDMAXB.read_GPSData()
                            data = ground.is_heading_goal(gps, des, pre_gps)
                            error_log.not_found_error_logger(phase, img_name, proc_img_name, p, not_found, data, pre_gps)
                        drive.forward()
                        time.sleep(5)
                        drive.stop()
                        pre_gps = gps
                        gps = GYSFDMAXB.read_GPSData()
                    # when the geomagnetic sensor is NOT enabled
                    else:
                        pre_gps = GYSFDMAXB.read_GPSData()
                        drive.forward()
                        time.sleep(5)
                        gps = GYSFDMAXB.read_GPSData()
                        data = ground.is_heading_goal(gps, des, pre_gps)
                        error_log.not_found_error_logger(phase, img_name, proc_img_name, p, not_found, data, pre_gps)
                        while data[3] != True: # Not heading the goal
                            if data[4] == 'Turn Right':
                                drive.turn_right()
                            elif data[4] == 'Turn Left':
                                drive.turn_left()
                            time.sleep(0.3)
                            pre_gps = gps
                            gps = GYSFDMAXB.read_GPSData()
                            data = ground.is_heading_goal(gps, des, pre_gps)
                            error_log.not_found_error_logger(phase, img_name, proc_img_name, p, not_found, data, pre_gps)
                        pre_gps = gps
                        gps = GYSFDMAXB.read_GPSData()
                # when GPS is NOT enabled
                else:
                    error_log.not_found_error_logger(phase, img_name, proc_img_name, p, not_found, [0]*15, [0,0], error_mag, error_heading)
                    drive.turn_right()
                    time.sleep(2)
                    drive.forward()
                    time.sleep(5)
                    drive.stop()
            drive.turn_right()
            time.sleep(1.7)
            drive.stop()
            continue
        # Change the time to advance according to the proximity of the goal
        time.sleep(4) if p < 0.01 else time.sleep(2)
        stuck, diff_distance = ground.is_stuck(pre_gps, gps, data[13])
        drive.stop()