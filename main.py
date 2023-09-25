from mavi1 import MAVI1
from modes import *
import time
import cv2

mavi:MAVI1 = MAVI1(led_count=88, led_brightness=1, angle_offset=(0, 0) , field_of_view_angle=82)

while True:

    MODE_find_target(mavi)
    print("Tick")

    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break
