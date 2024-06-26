import cv2
import datetime
import ArducamDepthCamera as ac
import numpy as np
from tof_distance import cal_distance_to_cone
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
import motor
import time

    
def detect_cone(cap, cam, inference_size, interpreter, labels, folder_path="../data/test/"):
    ret, frame = cap.read()
    if not ret:
        print('Cannot use camera1')
        return 0, 0, (0, 0), 0
    frame = cv2.resize(frame, inference_size)
    run_inference(interpreter, frame.tobytes())
    cones = get_objects(interpreter, 0.1)[:1] # set threshold
    detected_img, central_x, central_y, percent = append_objs_to_img(frame, inference_size, cones, labels)
    shape = detected_img.shape
    if central_x < shape[1] / 3:
        loc = "left"
    elif central_x > shape[1] * 2 / 3:
        loc = "right"
    elif percent < 15:
        loc = "not found"
    else:
        loc = "center"
    # cv2.imshow('frame', detected_img)
    now = datetime.datetime.now()
    cv2.imwrite(folder_path + now.strftime('%Y%m%d %H:%M:%S') + 'detected_img.jpg', detected_img) # 300x300
    if len(cones) != 0 and percent > 15:
        distance = cal_distance_to_cone(cam, central_x, central_y, detected_img.shape, folder_path)
    else:
        distance = np.nan
    return percent, distance, loc

    
def append_objs_to_img(img, inference_size, cones, labels):
    height, width, channels = img.shape
    scale_x, scale_y = width / inference_size[0], height / inference_size[1]
        
    # find the most reliable cone
    if len(cones) != 0:
        highest_confidence_cone = max(cones, key=lambda x: x.score)
        bbox = highest_confidence_cone.bbox.scale(scale_x, scale_y)
        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)
        central_x = (x0 + x1) / 2
        central_y = (y0 + y1) / 2
        percent = int(100 * highest_confidence_cone.score)
        label = '{}% {}'.format(percent, labels.get(highest_confidence_cone.id, highest_confidence_cone.id))

        img = cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        img = cv2.putText(img, label, (x0, y0+30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        return img, central_x, central_y, percent
    else:
        return img, np.nan, np.nan, 0

if __name__ == '__main__':
    cap = cv2.VideoCapture(1) # /dev/video1
    if cap.isOpened() == False:
        print("Error opening video stream or file")
    interpreter = make_interpreter('../model/red_cone.tflite')
    interpreter.allocate_tensors()
    labels = read_label_file('../model/red_cone.txt')
    inference_size = input_size(interpreter)
    
    cam = ac.ArducamCamera()
    if cam.open(ac.TOFConnect.CSI,0) != 0 :
        print("initialization failed")
    if cam.start(ac.TOFOutput.DEPTH) != 0 :
        print("Failed to start camera")
    #cam.setControl(ac.TOFControl.RANG, MAX_DISTANCE=4)
    # cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
    drive = motor.Motor()
    while cap.isOpened():
        percent, distance, loc = detect_cone(cap, cam, inference_size, interpreter, labels, folder_path="./")
        print("percent:", percent, "distance:", distance, "location:", loc)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # Goal judgment
        if distance < 0.30:
            print("Reach the goal")
            # phase = 4
            # reach_goal = True
            # img_proc_log.end_of_img_proc_phase()
            drive.forward()
            time.sleep(2.0)
            drive.stop()
            break
        elif distance < 4:
            drive.max_dutycycle = 65
        if loc == "right":
            drive.turn_right()
            time.sleep(0.3)
        elif loc == "left":
            drive.turn_left()
            time.sleep(0.3)
        elif loc == "not found":
            drive.forward()

    cap.release()
    cam.stop()
    cam.close()
    cv2.destroyAllWindows()