import cv2
import math
import numpy as np
import os
import random
import neopixel
import board
from gpiozero import DistanceSensor

class MAVI1:
    led_count:int = None 
    led_brightness:float = None #0-1

    angle_offset:tuple = None
    field_of_view_angle:int = None

    scaled_target_images = None
    video_capture = None #cv2.VideoCapture()

    led_strip = None
    ultrasonic_sensor = None
    gyro_sensor = None

    def __init__(self, led_count:int, led_brightness:float=1, angle_offset:tuple=(0,0), field_of_view_angle:int=90):
        self.led_count = led_count
        self.led_brightness = led_brightness

        self.angle_offset = angle_offset
        self.field_of_view_angle = field_of_view_angle
        
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.change_target("target.jpg")
        
        self.setup_gpio()

        print("started MAVI")

    def change_target(self, filename:str):
        filename = os.path.join(*[os.getcwd(), "static", "targets", filename] )
        target_img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

        self.scaled_target_images = []
        for scale in np.linspace(0.2, 1, )[::-1]:
            self.scaled_target_images.append(
                cv2.resize(
                    target_img, 
                    (int(target_img.shape[1] * scale), int(target_img.shape[0] * scale))
                )
            )
        print("changed Target")
        return True

    def get_angle_x(self):
        return (0 + self.angle_offset[0]) % 360

    def get_angle_y(self):
        return (0 + self.angle_offset[1]) % 360
    
    def get_angles(self):
        return (self.get_angle_x(), self.get_angle_y())

    def get_distance(self):
        return self.ultrasonic_sensor.distance
    
    def get_frame(self):
        return self.video_capture.read()

    def get_target(self, threshold:float=0.7):
        ret, frame = self.get_frame()

        if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame_size = (frame_gray.shape[1], frame_gray.shape[0])

            for target_scaled_image in self.target_scaled_images:
                # Use matchTemplate to find the object in the frame
                result = cv2.matchTemplate(frame_gray, target_scaled_image, cv2.TM_CCOEFF_NORMED)

                loc = np.where( result >= threshold)

                for position in zip(*loc[::-1]):
                    cv2.circle(frame, position, 5, (0, 255, 255), 2)
                    position_percent = (position[0] / frame_size[0] * 100, 100 - (position[1] / frame_size[1] * 100))
                    return [position_percent, True, frame]
        return [(0, 0), False, frame]

    
    def calculate_target_angles_from_img_position(self, position:tuple):
        angle_x = self.get_angle_x() - self.field_of_view_angle / 2 + self.field_of_view_angle * position[0] / 100
        angle_y = self.get_angle_y() - self.field_of_view_angle / 2 + self.field_of_view_angle * position[1] / 100

        angle_x = angle_x % 360
        angle_y = angle_y % 360

        return (angle_x, angle_y)

    def calculate_target_delta(self, current_angles:tuple, target_angles:tuple):
        delta_x = (target_angles[0] - current_angles[0]) % 360
        delta_y = (target_angles[1] - current_angles[1]) % 360

        return (delta_x, delta_y)

    def calculate_led_address_x1_plane(self, angle_x:float):
        angle_x = angle_x % 360
        address = angle_x / 360 * self.led_count
        return int(address)

    def calculate_led_address_sphere(self, delta_angles:tuple):
        delta_x, delta_y = delta_angles[0], delta_angles[1]

        x = (360 - delta_x) * -1 if delta_x > 180 else delta_x
        y = (360 - delta_y) * -1 if delta_y > 180 else delta_y

        rad = math.acos(y / math.sqrt(x*x + y*y))

        alpha = math.degrees(rad)
        alpha = 360 - alpha if x < 0 else alpha

        address = (alpha / 360) * self.led_count
        return int(address)

    def write_led(self, address:int, color:tuple):
        if address > self.led_count:
            return False
        else:
            address = (address + 6) % self.led_count
            self.strip[address] = color
            return True
        
    def write_leds(self, addresses:list, color:tuple):
        for address in addresses:
            if not self.write_led(address, color):
                return False
        return True

    def write_led_strip(self, color):
        self.strip.fill(color)
        return True

    def setup_gpio(self):
        self.led_strip = neopixel.NeoPixel(board.D18, self.led_count)  #LED-Strip: LED Pin 30
        self.ultrasonic_sensor = DistanceSensor(echo=17, trigger=4)             #Ultrasonic-Sensor: ECHO Pin 17; Trigger Pin 4
        return True
