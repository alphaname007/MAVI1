import cv2
import math
#import neopixel
#import board
#from gpiozero import DistanceSensor

led_count:int = None 
led_brightness:float = None # 0-1

threshold:float = None

field_of_view_angle:int = None

angle_center_cone_angle:float = None #0-1

target_img = None

video_capture = None

led_strip = None
ultrasonic_sensor = None
gyro_sensor = None

def __init__(self, led_count:int, led_brightness:float=1, threshold:float=0.6, target_file:str="target.jpg",  field_of_view_angle:int=90, angle_center_cone_angle:int=10):
    self.led_count = led_count
    self.led_brightness = led_brightness
    self.threshold = threshold
    self.target_img = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
    self.field_of_view_angle = field_of_view_angle
    self.angle_center_cone_angle = angle_center_cone_angle
    self.video_capture = cv2.VideoCapture(1)
    #setup_gpio()



def get_angle_x(self):
    return 270

def get_angle_y(self):
    return 120

def get_target_position_from_img(self):
    ret, frame = self.video_capture.read()

    if ret:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    return (50, 50)


def calculate_target_angles_from_img_position(self, position:tuple):
    angle_x = get_angle_x() - field_of_view_angle / 2 + field_of_view_angle * position[0]
    angle_y = get_angle_y() - field_of_view_angle / 2 + field_of_view_angle * position[1]
    return (angle_x, angle_y)

def calculate_led_address_x1_x2_plane(self, angle_x:float, offset:float=0):
    angle_x = angle_x + offset if angle_x + offset <= 360 else angle_x + offset - 360
    return int((angle_x / 360) * self.led_count)

def calculate_led_address_sphere(self, current_angles:tuple, target_angles:tuple, offset:float=0):
    delta_x = current_angles[0] - target_angles[0]
    delta_y = current_angles[1] - target_angles[1]

    if delta_x == 0:
        delta_x = 0.00000001

    alpha = math.tan(delta_y / delta_x)

    address = alpha / 360 * self.led_count
    return address



def write_led_strip(self, color):
    self.strip.fill(color)
    return True

def get_distance(self):
    return ultrasonic_sensor.distance

def setup_gpio(self):
    self.led_strip = neopixel.NeoPixel(board.D18, 30, self.led_brightness)  #LED-Strip: LED Pin 30
    self.ultrasonic_sensor = DistanceSensor(echo=17, trigger=4)                  #Ultrasonic-Sensor: ECHO Pin 17; Trigger Pin 4
    return True