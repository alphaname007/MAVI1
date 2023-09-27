import time
import cv2

def MODE_find_target(mavi, threshold:float=0.7, spotted_angles:int=10):
    position, found, frame = mavi.get_target()

    cv2.imshow("frame", frame)
    
    if 38 <= position[0] <= 62 and 38 <= position[1] <= 62:
        mavi.write_led_strip((0,255,0))
        print("Target spotted")
        return (True, "spotted")


    if not found:
        mavi.write_led_strip((255,0,0))
        return (False, "not found")
    
    else:
        target_angles = mavi.calculate_target_angles_from_img_position(position) #Could be used to store the last known target position
        delta_angles = mavi.calculate_target_delta(mavi.get_angles(), target_angles)

        address = mavi.calculate_led_address_sphere(delta_angles)
        mavi.write_led(address, (0,0,255))
        return(True, "found")

def MODE_use_compass(mavi):
    mavi.write_led(mavi.calculate_led_address_x1_plane(mavi.get_angle_x), (0,0,255))

def MODE_distance(mavi, inner_boundary:float=0.5, outer_boundary:float=2):
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
    print("started Glasses")
