import cv2
import numpy as np 
# New
print("What a sommelier!")

# OPENING THE IMAGE
#cap = cv2.VideoCapture(0) 
frame=cv2.imread("test2.jpg")

# thresholds for filtering out the random colours
lower_red1 = np.array([155, 30, 100])
upper_red1 = np.array([180,255,255])
lower_red2 = np.array([0, 30, 100])
upper_red2 = np.array([25,255,255])
lower_blue = np.array([90, 30, 50]) 
upper_blue = np.array([140, 255, 255]) 
