import time
import cv2

def MODE_find_target(mavi, threshold:float=0.6, spotted_angles:int=10):
    position, found, frame = mavi.get_target()

    cv2.imshow("frame", frame)
    
    if not found:
        mavi.write_led_strip((255,0,0))
        return
    else:
        target_angles = mavi.calculate_target_angles_from_img_position(position) #Could be used to store the last known target position
        delta_angles = mavi.calculate_target_delta(mavi.get_angles(), target_angles)
        if delta_angles[0] < spotted_angles and delta_angles[1] < spotted_angles:
            mavi.write_led_strip((0,255,0))
            return
        else:
            address = mavi.calculate_led_address_sphere(delta_angles)
            mavi.write_led(address, (0,0,255))




def MODE_find_target_on_camera(mavi):
    position, found, frame = mavi.get_target()

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

def MODE_compass(mavi):
    mavi.write_led(mavi.calculate_led_address_x1_plane(mavi.get_angle_x), (0,0,255))

def MODE_distance(mavi, inner_boundary:int=50, outer_boundary:int=200):
    distance = mavi.get_distance()
    percent = inner_boundary / outer_boundary * 100

    start_address_right = int(mavi.led_count / 4 - mavi.led_count / 4 * percent / 100)
    start_address_left = int(mavi.led_count * 3 / 4 - mavi.led_count / 4 * percent / 100)
    
    end_address_right = int(mavi.led_count / 4 + mavi.led_count / 4 * percent / 100)
    end_address_left = int(mavi.led_count * 3 / 4 + mavi.led_count / 4 * percent / 100)
    
    addresses = list(range(start_address_right, end_address_right)) + list(range(start_address_left, end_address_left))
    mavi.write_leds(addresses,  (0,0,255))

def MODE_start_up(mavi):
    mavi.write_led_strip((0,0,0))
    color_change = 255 / mavi.led_count
    for i in range(0, mavi.led_count):
        mavi.write_led(i, (int(i*color_change), 0, 255-int(i*color_change)))
        time.sleep(100/1000)
