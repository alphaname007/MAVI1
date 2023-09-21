import cv2
import numpy as np

threshold = 0.5


# Capture the webcam feed
cap = cv2.VideoCapture(0)

# Load the image of the object you want to track
target_img = cv2.imread('target.jpg')
target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

# Get the width and height of the template
w, h = target_img.shape[::-1]

while True:
    # Read a frame from the webcam feed
    ret, frame = cap.read()

    if ret:
        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        # Use matchTemplate to find the object in the frame
        result = cv2.matchTemplate(frame_gray, target_img, cv2.TM_CCOEFF_NORMED)

        loc = np.where( result >= threshold)
        
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        # Show the frame with the object highlighted
        cv2.imshow('frame', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
