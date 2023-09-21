import cv2
import time
import numpy as np

leds_count = 20

target_img = cv2.imread("target.jpg", cv2.IMREAD_GRAYSCALE)

video = cv2.VideoCapture(1)

target_position = (50, 50) # x|y in percent

frequency = 500 #in ms


def get_target_position(threshold:float=0.95):
    #_, frame = video.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.imread("Test.jpg", cv2.IMREAD_GRAYSCALE)
    
    w, h = frame.shape[::-1]


    result = cv2.matchTemplate(target_img, frame, cv2.TM_CCOEFF_NORMED)[0]
    
    loc = np.where( result >= threshold)

    for pt in zip(*loc[::-1]):
        print("found")
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    
    cv2.imshow("Test", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (0, 0)

def write_leds(position:tuple):
    return True

while True:
    time.sleep(frequency/1000)

    target_position = get_target_position()

    write_leds(target_position)