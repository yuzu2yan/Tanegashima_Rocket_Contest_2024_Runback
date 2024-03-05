import argparse
import cv2
import os

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

    
def detect_cone():
    cap = cv2.VideoCapture(1) # /dev/video1
    if cap.isOpened():
        ret, frame = cap.read()
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    interpreter = make_interpreter('../../model/red_cone.tflite')
    interpreter.allocate_tensors()
    labels = read_label_file('../../model/red_cone.txt')
    inference_size = input_size(interpreter)
    img_rgb = cv2.resize(img_rgb, inference_size)
    run_inference(interpreter, img_rgb.tobytes())
    cones = get_objects(interpreter, 0.1)[:1] # set threshold
    detected_img, x, y, percent = append_objs_to_img(img_rgb, inference_size, cones, labels)
    
    # cv2.imshow('frame', detected_img)
    cv2.imwrite('detected_img.jpg', detected_img)
    # height, width, channels = detected_img.shape
    print("x : ", x, "y : ", y, "percent : ", percent)
    cap.release()
    # cv2.destroyAllWindows()
    return x, y, percent

    
def append_objs_to_img(img, inference_size, cones, labels):
    height, width, channels = img.shape
    scale_x, scale_y = width / inference_size[0], height / inference_size[1]
        
    # 最も信頼度の高いオブジェクトを見つける
    highest_confidence_cone = max(cones, key=lambda x: x.score)
    bbox = highest_confidence_cone.bbox.scale(scale_x, scale_y)
    x0, y0 = int(bbox.xmin), int(bbox.ymin)
    x1, y1 = int(bbox.xmax), int(bbox.ymax)
    center_x, center_y = int((x0 + x1) / 2), int((y0 + y1) / 2)
    
    percent = int(100 * highest_confidence_cone.score)
    label = '{}% {}'.format(percent, labels.get(highest_confidence_cone.id, highest_confidence_cone.id))

    img = cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
    img = cv2.putText(img, label, (x0, y0+30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        
    return img, center_x, center_y, percent

if __name__ == '__main__':
    # while True:
    detect_cone()

        