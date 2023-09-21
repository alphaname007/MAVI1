from mavi1 import MAVI1

import time

mavi:MAVI1 = MAVI1(20, 1, 0.6, target_file="target.jpg")

while True:
    time.sleep(1)
    print(mavi.get_target_position_from_img())