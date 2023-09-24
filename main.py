from mavi1 import MAVI1

import time
import cv2

mavi:MAVI1 = MAVI1(led_count=88, led_brightness=1, threshold=0.6, target_file="target.jpg", field_of_view_angle=82)

while True:

    MODUS_find_target()

    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break
