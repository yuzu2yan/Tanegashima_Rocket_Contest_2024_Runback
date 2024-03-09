import datetime
import csv

"""
phase 1 : Floating
      2 : Ground 
      3 : Image Processing
      4 : Reach the goal
"""

class FloatingLogger(object):
    filename = ''
    state = 'None'
    """
    state Rising
          Ascent Completed
          Landing
          Error
    """

    def __init__(self, directory_path):
        now = datetime.datetime.now()
        FloatingLogger.filename = directory_path + 'floating.csv'
        with open(FloatingLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'state', 'pressure', 'temperature', 'altitude', 'description'])
        f.close()
    
    def floating_logger(self, data):
        with open(FloatingLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state] + data)
        f.close()
        
    def end_of_floating_phase(self, description='Separation mechanism activated'):
        with open(FloatingLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state, '', '', '', description])
        f.close()
        
class GroundLogger(object):
    filename = ''
    state = 'None'
    """
    state Normal
          Stuck
          Something Wrong
    """
    
    def __init__(self, directory_path):
        now = datetime.datetime.now()
        GroundLogger.filename = directory_path + 'ground.csv'
        with open(GroundLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            # calib status : 0 ~ 3
            writer.writerow(['time', 'state', 'distance to goal', 'destination angle', 'heading angle','angle difference', 'heading goal', 'direction', 'longtitude', 'latitude', 'magX', 'magY', 'magZ', 'accelX', 'accelY', 'accelZ', 'accel', 'calib status mag', 'calib status accel'])
        f.close()
    
    def ground_logger(self, data, distance):
        with open(GroundLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), self.state, distance] + data)

    def end_of_ground_phase(self):
        with open(GroundLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'Start Image Processing'])
        f.close()
        
class ImgProcLogger(object):
    filename = ''
    """
    cone location center
                  right
                  left
                  not found
    """
    def __init__(self, directory_path):
        now = datetime.datetime.now()
        ImgProcLogger.filename = directory_path + 'img_proc.csv'
        with open(ImgProcLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'cone place', 'distance to goal', 'percent', 'ditected img name', 'tof image name'])
        f.close()
        
    def img_proc_logger(self, cone_place, distance, percent, ditected_img_name, tof_img_name):
        with open(ImgProcLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), cone_place, distance, percent, ditected_img_name, tof_img_name])
        f.close()    
    
    def end_of_img_proc_phase(self):
        with open(ImgProcLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), 'Reach the goal'])
        f.close()
        
class ErrorLogger(object):
    filename = ''
    """
    phase Floating
          Ground
          Image Processing
    """
    def __init__(self, directory_path):
        now = datetime.datetime.now()
        ErrorLogger.filename = directory_path + 'error.csv'
        with open(ErrorLogger.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime('%Y%m%d %H:%M:%S')])
            writer.writerow(['time', 'phase', 'error description', 'data'])
        f.close()
        
    def baro_error_logger(self, phase, data):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'Altitude value decreases during ascent','pressure', data[0], 'temperature', data[1],'altitude', data[2]])
        f.close()
        
    def img_proc_error_logger(self, phase, distance=0):
        with open(ErrorLogger.filename, 'a') as f:
            now = datetime.datetime.now()
            writer = csv.writer(f)
            writer.writerow([now.strftime('%H:%M:%S'), phase, 'distance', distance, 'Image processing failed'])
        f.close()
        
    # def not_found_error_logger(self, phase):
    #     with open(ErrorLogger.filename, 'a') as f:
    #         now = datetime.datetime.now()
    #         writer = csv.writer(f)
    #         writer.writerow([now.strftime('%H:%M:%S'), phase, 'Cone not found', 'img name', img_name, 'processed img name', proc_img_name, 'percentage of cone in img', p, 'not found counter', not_found, 'destination angle', data[0], 'heading angle', data[1],'angle difference', data[2], 'heading goal', data[3], 'direction', data[4], 'longtitude', data[5], 'latitude', data[6], 'previous longtitude', pre_gps[0], 'previous latitude', pre_gps[1], 'magX', data[7], 'magY', data[8], 'magZ', data[9], 'accelX', data[10], 'accelY', data[11], 'accelZ', data[12], 'accel', data[13], 'calib status mag', data[14], 'calib status accel', data[15], 'error geomagnetic sensor', error_mag, 'error heading counter', error_heading])
    #     f.close()
        