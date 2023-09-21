import cv2
import math
import neopixel
import board

led_count:int = None 
led_brightness:float = None # 0-1
target_img = None
video_capture = None
led_strip = None

def __init__(self, led_count:int, led_brightness:float, target_file:str):
    self.led_count = led_count
    self.led_brightness = led_brightness
    self.target_img = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
    self.video_capture = cv2.VideoCapture(1)
    setup_gpio()
    

def get_target_position(self):
    return (50, 50)

def calculate_led_address(self, position:tuple):
    x = (position[0] - 50) / 50
    y = (position[1] - 50) / 50

    return int((self.led_count / 360) * math.tan(y / x))

def write_led(self, address:int, color):
    self.strip[address] = color
    return True

def setup_gpio(self):
    self.led_strip = neopixel.NeoPixel(board.D18, 30, self.led_brightness) #LED_Pin 30