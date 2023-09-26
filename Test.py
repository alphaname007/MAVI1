from mavi1 import MAVI1

mavi:MAVI1 = MAVI1(led_count=27)

mavi.setup_gpio()

mavi.write_led_strip()
