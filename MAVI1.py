import cv2
import math
import neopixel
import board

from gpiozero import DistanceSensor

led_count:int = None 
led_brightness:float = None # 0-1

center_box_radius:float = None #0-1

target_img = None

video_capture = None

led_strip = None
ultrasonic_sensor = None
gyro_sensor = None

def __init__(self, led_count:int, led_brightness:float=1, target_file:str="target.jpg", center_box_radius:float=0.25):
    self.led_count = led_count
    self.led_brightness = led_brightness
    self.target_img = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
    self.center_box_radius = center_box_radius
    self.video_capture = cv2.VideoCapture(1)
    setup_gpio()
    

def get_target_position(self):
    return (50, 50)

def calculate_led_address(self, position:tuple):
    x = (position[0] - 50) / 50
    y = (position[1] - 50) / 50

    if center_box_radius * (-1) <= x <= center_box_radius and center_box_radius * (-1) <= y <= center_box_radius:
        return (True)
    else:
        address = int((self.led_count / 360) * math.tan(y / x))
        return (False, address)

def write_led(self, address:int, color):
    self.strip[address] = color
    return True

def write_led_strip(self, color):
    self.strip.fill(color)
    return True

def get_distance(self):
    return ultrasonic_sensor.distance

def setup_gpio(self):
    self.led_strip = neopixel.NeoPixel(board.D18, 30, self.led_brightness)  #LED-Strip: LED Pin 30
    self.ultrasonic_sensor = DistanceSensor(echo=17, trigger=4)                  #Ultrasonic-Sensor: ECHO Pin 17; Trigger Pin 4
    return True