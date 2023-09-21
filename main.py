import MAVI1

import time

mavi:MAVI1 = MAVI1(leds_count=20, target_file="target.jpg")

frequency = 500

while True:
    time.sleep(frequency/1000)

    target_position = mavi.get_target_position()

    led_address = mavi.calculate_led_address(target_position)

    mavi.write_led(led_address, (255, 0, 0))