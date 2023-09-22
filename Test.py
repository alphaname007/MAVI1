from mavi1 import MAVI1

import time
import cv2

mavi:MAVI1 = MAVI1(20, 1, 0.6, target_file="target.jpg")

while True:
    ret = mavi.get_target()

    position = ret[0]
    found = ret[1]
    frame = ret[2]

    print(found, position)

    if found:
        mavi.speak("Object detected")

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break

    print()