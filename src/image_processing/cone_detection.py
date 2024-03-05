import argparse
import cv2
import os
from tof_distance import cal_distance_to_cone

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

    
def detect_cone():
    cap = cv2.VideoCapture(1) # /dev/video1
    if cap.isOpened():
        ret, frame = cap.read()
        print(frame.shape)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        print("Error opening video stream or file")
        return 0, 0, 0
    interpreter = make_interpreter('../../model/red_cone.tflite')
    interpreter.allocate_tensors()
    labels = read_label_file('../../model/red_cone.txt')
    inference_size = input_size(interpreter)
    img_rgb = cv2.resize(img_rgb, inference_size)
    run_inference(interpreter, img_rgb.tobytes())
    cones = get_objects(interpreter, 0.1)[:1] # set threshold
    detected_img, central_x, central_y, percent = append_objs_to_img(img_rgb, inference_size, cones, labels)
    
    cv2.imshow('frame', detected_img)
    cv2.imwrite('detected_img.jpg', detected_img) # 300x300
    cap.release()
    # cv2.destroyAllWindows()
    if len(cones) != 0 and percent > 30:
        distance = cal_distance_to_cone(central_x, central_y, detected_img.shape)
    else:
        distance = 100
    return percent, distance

    
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
        return img, 0, 0, 0

if __name__ == '__main__':
    while True:
        percent, distance = detect_cone()
        print("percent:", percent, "distance:", distance)

        