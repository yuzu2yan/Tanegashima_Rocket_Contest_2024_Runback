import sys
import cv2
import numpy as np
import ArducamDepthCamera as ac


MAX_DISTANCE = 4

def process_frame(depth_buf: np.ndarray, amplitude_buf: np.ndarray) -> np.ndarray:
        
    depth_buf = np.nan_to_num(depth_buf)

    amplitude_buf[amplitude_buf<=7] = 0
    amplitude_buf[amplitude_buf>7] = 255

    depth_buf = (1 - (depth_buf/MAX_DISTANCE)) * 255
    depth_buf = np.clip(depth_buf, 0, 255)
    result_frame = depth_buf.astype(np.uint8)  & amplitude_buf.astype(np.uint8)
    return result_frame 
        
def usage(argv0):
    print("Usage: python "+argv0+" [options]")
    print("Available options are:")
    print(" -d        Choose the video to use")

def cal_distance_to_cone(x, y, shape):
    distance = 100
    x = int(x * 240 / shape[1])
    y = int(y * 180 / shape[0])
    start_x = x - 4 if x - 4 > 0 else 0
    start_y = y - 4 if y - 4 > 0 else 0
    end_x = x + 4 if x + 4 < 240 else 240
    end_y=  y + 4 if y + 4 < 180 else 180
    
    cam = ac.ArducamCamera()
    if cam.open(ac.TOFConnect.CSI,0) != 0 :
        print("initialization failed")
    if cam.start(ac.TOFOutput.DEPTH) != 0 :
        print("Failed to start camera")
    cam.setControl(ac.TOFControl.RANG,MAX_DISTANCE)
    # cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)

    frame = cam.requestFrame(200)
    if frame != None:
        depth_buf = frame.getDepthData()
        amplitude_buf = frame.getAmplitudeData()
        cam.releaseFrame(frame)
        amplitude_buf*=(255/1024)
        amplitude_buf = np.clip(amplitude_buf, 0, 255)

        # cv2.imshow("preview_amplitude", amplitude_buf.astype(np.uint8))
        # cv2.imwrite('amplitude.jpg', amplitude_buf.astype(np.uint8))
        distance = np.mean(depth_buf[start_y:end_y,start_x:end_x])
        # print("distance to cone:",distance)
        result_image = process_frame(depth_buf,amplitude_buf)
        result_image = cv2.applyColorMap(result_image, cv2.COLORMAP_JET)
        cv2.rectangle(result_image,(start_x,start_y),(end_x,end_y),(128,128,128), 1)
        
        # cv2.imshow("preview",result_image)
        cv2.imwrite('result.jpg', result_image)
        cam.stop()
        cam.close()
        sys.exit(0)
    return distance


if __name__ == "__main__":
    x = 120
    y = 90
    print(cal_distance_to_cone(x,y))