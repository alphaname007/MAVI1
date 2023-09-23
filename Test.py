from mavi1 import MAVI1

import time
import cv2

mavi:MAVI1 = MAVI1(led_count=88, led_brightness=1, threshold=0.6, target_file="target.jpg", field_of_view_angle=82)

def MODUS_find_target():
    ret = mavi.get_target()

    position = ret[0]
    found = ret[1]
    frame = ret[2]

    position_x, position_y = position

    cv2.imshow("MODUS_find_target", frame)

    if not found:
        print("no target available")
        mavi.write_led_strip((255, 0, 0))
        return

    mavi.write_led_strip((0,0,0))

    if 15 <= position_x <= 85 and 85 <= position_y: #top
        print("target in TOP")
        return mavi.write_leds(list(range(int(mavi.led_count-mavi.led_count/10) , mavi.led_count)) + list(range(0, int(mavi.led_count/10))), (0,0,255))
    
    elif 15 <= position_x <= 85 and 15 >= position_y: #bottom
        print("target in BOTTOM")
        return mavi.write_leds(list(range(int(mavi.led_count/40) , int(mavi.led_count/60))), (0,0,255))
    
    elif 15 >= position_x and 85 <= position_y: #top-left
        print("target in TOP-LEFT")
        return mavi.write_leds(list(range(int(mavi.led_count/80) , int(mavi.led_count/90))), (0,0,255))
    
    elif 85 <= position_x and 85 <= position_y: #top-right
        print("target in TOP-RIGHT")
        return mavi.write_leds(list(range(int(mavi.led_count/10) , int(mavi.led_count/20))), (0,0,255))
    
    elif 40 >= position_x and 15 <= position_y <= 85: #left
        print("target in LEFT")
        return mavi.write_leds(list(range(int(mavi.led_count/70) , int(mavi.led_count/80))), (0,0,255))
    
    elif 60 <= position_x and 15 <= position_y <= 85: #right
        print("target in RIGHT")
        return mavi.write_leds(list(range(int(mavi.led_count/20) , int(mavi.led_count/30))), (0,0,255))

    elif 15 >= position_x and 15 >= position_y: #bottom-left
        print("target in BOTTOM-LEFT")
        return mavi.write_leds(list(range(int(mavi.led_count/60) , int(mavi.led_count/70))), (0,0,255))

    elif 85 <= position_x and 15 >= position_y: #bottom-right
        print("target in BOTTOM-RIGHT")
        return mavi.write_leds(list(range(int(mavi.led_count/30) , int(mavi.led_count/40))), (0,0,255))
    
    else:
        print("target SPOTTED")
        return mavi.write_led_strip((0, 255, 0))

def MODUS_compass():
    return mavi.write_led(mavi.calculate_led_address_x1_plane(mavi.get_angle_x), (0,0,255))

def MODUS_start_up():
    mavi.write_led_strip((0,0,0))
    color_change = 255 / mavi.led_count
    for i in range(0, mavi.led_count):
        mavi.write_led(i, (int(i*color_change), 0, 255-int(i*color_change)))
        time.sleep(100/1000)


while True:

    MODUS_find_target()

    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break