from mavi1 import MAVI1

import time
import cv2

mavi:MAVI1 = MAVI1(led_count=88, led_brightness=1, field_of_view_angle=82)

print(mavi.calculate_led_address_sphere((270, -90)))