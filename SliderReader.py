import cv2
import numpy as np

img = cv2.imread('putting.jpg')

# Method 1: copy image and set other channels to black
r = img.copy()
r[:,:,0] = r[:,:,1] = 0

g = img.copy()
g[:,:,0] = g[:,:,2] = 0

b = img.copy()
b[:,:,1] = b[:,:,2] = 0

cv2.imshow("red",r)
cv2.imshow("green",g)
cv2.imshow("blue",b)
cv2.waitKey(0)
cv2.destroyAllWindows()
