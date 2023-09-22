import os
import cv2
import math
import numpy as np
from gtts import gTTS
from pygame import mixer
from threading import Thread
##import neopixel
#import board
#from gpiozero import DistanceSensor

class MAVI1:
    led_count:int = None 
    led_brightness:float = None # 0-1

    threshold:float = None

    field_of_view_angle:int = None

    angle_center_cone_angle:float = None #0-1

    target_img = None

    video_capture = None

    speaker_language = None
    speaker_volume = None

    False

    mixer.init()

    led_strip = None
    ultrasonic_sensor = None
    gyro_sensor = None

    def __init__(self, led_count:int, led_brightness:float=1, threshold:float=0.6, target_file:str="target.jpg",  field_of_view_angle:int=90, angle_center_cone_angle:int=10, speaker_volume=0.2, speaker_language="en"):
        self.led_count = led_count
        self.led_brightness = led_brightness
        self.threshold = threshold
        self.target_img = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
        self.field_of_view_angle = field_of_view_angle
        self.angle_center_cone_angle = angle_center_cone_angle
        self.video_capture = cv2.VideoCapture(0)
        self.speaker_language = speaker_language
        self.speaker_volume = speaker_volume
        #setup_gpio()



    def get_angle_x(self):
        return 270

    def get_angle_y(self):
        return 120

    def get_distance(self):
        return ultrasonic_sensor.distance
    
    def get_target(self):
        ret, frame = self.video_capture.read()

        scales = np.linspace(0.2, 1.0, 20)[::-1]

        if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame_size = (frame_gray.shape[1], frame_gray.shape[0])

            for scale in scales:
                # Resize the object according to the scale
                resized_obj = cv2.resize(self.target_img, (int(self.target_img.shape[1] * scale), int(self.target_img.shape[0] * scale)))

                # Use matchTemplate to find the object in the frame
                result = cv2.matchTemplate(frame_gray, resized_obj, cv2.TM_CCOEFF_NORMED)

                loc = np.where( result >= self.threshold)

                cv2.imshow('frame', frame)

                for position in zip(*loc[::-1]):
                    cv2.circle(frame, position, 5, (0, 255, 255), 2)
                    return [(position[0] / frame_size[0] * 100, position[1] / frame_size[1] * 100), True, frame]
        return [(0, 0), False, frame]

    
    def calculate_target_angles_from_img_position(self, position:tuple):
        angle_x = self.get_angle_x() - self.field_of_view_angle / 2 + self.field_of_view_angle * position[0]
        angle_y = self.get_angle_y() - self.field_of_view_angle / 2 + self.field_of_view_angle * position[1]
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


    def write_led(self, address:int, color:tuple):
        if address > self.led_count:
            return False
        else:
            self.strip[address] = color
            return True

    def write_led_strip(self, color):
        self.strip.fill(color)
        return True
    
    def speak(self, text:str):
        if not self._speaking:
            speaker_thread = Thread()


    def _speak(self, text:str):
        if not self._speaking:
            self._speaking = True
            spoken = gTTS(text=text, lang=self.speaker_language, slow=False)
            spoken.save("tmp.mp3")
            mixer.music.load("tmp.mp3")
            mixer.music.set_volume(self.speaker_volume)
            mixer.music.play()
            os.remove("tmp.mp3")
            self._speaking = False
        


    def setup_gpio(self):
        self.led_strip = neopixel.NeoPixel(board.D18, 30, self.led_brightness)  #LED-Strip: LED Pin 30
        self.ultrasonic_sensor = DistanceSensor(echo=17, trigger=4)                  #Ultrasonic-Sensor: ECHO Pin 17; Trigger Pin 4
        return True