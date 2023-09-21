import MAVI1

import time

mavi:MAVI1 = MAVI1(leds_count=20, target_file="target.jpg")

frequency = 500

while True:
    time.sleep(frequency/1000)

    target_position = mavi.get_target_position()

    in_center, led_address = mavi.calculate_led_address(target_position)

    if in_center:
        mavi.write_led_strip(0, 0, 255)
    else:
        mavi.write_led(led_address, (255, 0, 0))