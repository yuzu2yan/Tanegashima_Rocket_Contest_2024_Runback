import bno055
import gnss
from geographiclib.geodesic import Geodesic 
import math
import time
import motor
import numpy as np
import datetime
import csv


def cal_azimuth(lng1, lat1, lng2, lat2):
    lng1 = math.radians(lng1)
    lat1 = math.radians(lat1)
    lng2 = math.radians(lng2)
    lat2 = math.radians(lat2)
    dx = lng2 - lng1
    des_ang = 90 - math.degrees(math.atan2(math.cos(lat1)*math.tan(lat2)-math.sin(lat1)*math.cos(dx), math.sin(dx)))
    if des_ang < 0:
        des_ang += 360
    """
    https://keisan.casio.jp/exec/system/1257670779
    PointA(lng x1, lat y1), PointB(lng x2, lat y2)
            (gps_lng, gps_lat),     (des_lng, des_lat)
    ϕ = 90 - atan2(cosy1tany2 - siny1cosΔx, sinΔx)
    Δx = x2 - x1
    """
    return des_ang

def cal_distance(x1, y1, x2, y2):
    distance = Geodesic.WGS84.Inverse(y1, x1, y2, x2)['s12'] # [m]
    return distance

def cal_heading_ang():
    try:
        data = bno055.read_Mag_AccelData()
        """
        data = [magX, magY, magZ, accelX, accelY, accelZ, accel, calib_mag, calib_accel]
        """
        hearding_ang = np.degrees(np.arctan2(data[1], data[0]))
        if hearding_ang < 0:
            hearding_ang += 360
        return hearding_ang, data
    except Exception as e:
        print("Error : Can't read Mag data")
        with open('sys_error.csv', 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), "Can't read Mag data", str(e)])
            f.close()
        return 0, [0, 0, 0, 0, 0, 0, 0, 0, 0]

def is_heading_goal(gps, des):
    des_ang = cal_azimuth(gps[0], gps[1], des[0], des[1])
    print("des_ang : ", des_ang)
    heading_ang, data = cal_heading_ang()
    print("heading_ang : ", heading_ang)
    ang_diff = abs(des_ang - heading_ang)
    if ang_diff < 15 or 335 < ang_diff:
        return [des_ang, heading_ang, ang_diff, True, "Go Straight"] + gps + data
    else:
        if ((heading_ang > des_ang and ang_diff < 180) or (heading_ang < des_ang and ang_diff > 180)):
            return [des_ang, heading_ang, ang_diff, False, "Turn Left"] + gps + data
        else:
            return [des_ang, heading_ang, ang_diff, False, "Turn Right"] + gps + data

# destination point(lon, lat)
des = [0,0]


if __name__ == '__main__':
    drive = motor.Motor()
    while True:
        drive.forward()
        gps = gnss.read_GPSData()
        distance = cal_distance(gps[0], gps[1], des[0], des[1])
        print("distance :", distance)
        if distance < 3:
            print("end")
            drive.stop()
            break
        time.sleep(0.2)
        data = is_heading_goal(gps, des)
        if data[3] == True:
            print("Heading Goal!!")
        else:
            if data[4] == 'Turn Right':
                drive.turn_right()
            elif data[4] == 'Turn Left':
                drive.turn_left()
        time.sleep(0.5)