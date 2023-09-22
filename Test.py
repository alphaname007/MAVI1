from mavi1 import MAVI1

import time
import cv2

mavi:MAVI1 = MAVI1(4, 1, 0.6, target_file="target.jpg")

while True:
    ret = mavi.get_target()

    position = ret[0]
    found = ret[1]
    frame = ret[2]

    target_angles = mavi.calculate_target_angles_from_img_position(position)
    
    current_angles = mavi.get_angles()

    delta_angles = mavi.calculate_target_delta(current_angles, target_angles)

    address = mavi.calculate_led_address_sphere(delta_angles)

    print(f"Target:{found}, \t img_position {position}, \t delta_angles {delta_angles}, \t address {address}")

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break

    print()