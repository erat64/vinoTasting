import cv2 
import numpy as np 
import csv
# OPENING THE IMAGE
#cap = cv2.VideoCapture(0) 
frame=cv2.imread("multi.jpg")

# FILTERING THE IMAGE
# It converts the BGR color space of image to HSV color space 
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

# thresholds for filtering out the random colours
lower_red1 = np.array([155, 80, 100])
upper_red1 = np.array([180,255,160])
lower_red2 = np.array([0, 80, 100])
upper_red2 = np.array([25,255,160])
lower_blue = np.array([90, 30, 50]) 
upper_blue = np.array([140, 255, 255])
lower_green = np.array([35, 20, 50]) 
upper_green = np.array([90, 255, 255]) 

# filtering the image for colours
maska = cv2.inRange(hsv, lower_red1, upper_red1)
maskb = cv2.inRange(hsv, lower_red2, upper_red2)
maskred = cv2.add(maska,maskb)
maskblue = cv2.inRange(hsv, lower_blue, upper_blue)
maskgreen = cv2.inRange(hsv, lower_green, upper_green)

kernel = np.ones((4,4),np.float32)/16
maskred = cv2.filter2D(maskred,-1,kernel)
maskred = cv2.filter2D(maskred,-1,kernel)
maskred = cv2.filter2D(maskred,-1,kernel)
maskred = cv2.filter2D(maskred,-1,kernel)
maskred = cv2.filter2D(maskred,-1,kernel)
ret,maskred = cv2.threshold(maskred,127,255,cv2.THRESH_BINARY)

kernel = np.ones((5,5),np.float32)/25
maskblue = cv2.filter2D(maskblue,-1,kernel)
maskblue = cv2.filter2D(maskblue,-1,kernel)
ret,maskblue = cv2.threshold(maskblue,127,255,cv2.THRESH_BINARY)

kernel = np.ones((5,5),np.float32)/25
maskgreen = cv2.filter2D(maskgreen,-1,kernel)
maskgreen = cv2.filter2D(maskgreen,-1,kernel)
maskgreen = cv2.filter2D(maskgreen,-1,kernel)
ret,maskgreen = cv2.threshold(maskgreen,127,255,cv2.THRESH_BINARY)

# DETECTING THE CENTROIDS
_,img = cv2.threshold(maskblue,0,255,cv2.THRESH_OTSU)
h, w = img.shape[:2]
centriods, contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
moments  = [cv2.moments(cnt) for cnt in contours0]
# Rounded the centroids to integer.
blues = [( int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ) for m in moments]
print('blues:', blues)
# DETECTING THE CENTROIDS
_,img = cv2.threshold(maskgreen,0,255,cv2.THRESH_OTSU)
h, w = img.shape[:2]
centriods, contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
moments  = [cv2.moments(cnt) for cnt in contours0]
# Rounded the centroids to integer.
greens = [( int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ) for m in moments]
print('greens:', greens)
# DETECTING THE CENTROIDS
_,img = cv2.threshold(maskred,0,255,cv2.THRESH_OTSU)
h, w = img.shape[:2]
centriods, contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
moments  = [cv2.moments(cnt) for cnt in contours0]
# Rounded the centroids to integer.
reds = [( int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ) for m in moments]
print('reds:', reds)

answers=[]
for i in reds:
    answers.append(["a",i[1]])
for i in blues:
    answers.append(["b",i[1]])
for i in greens:
    answers.append(["c",i[1]])

answers=sorted(answers, key=lambda x : x[1])
answers=[i[0] for i in answers]
print(answers)
# DISPLAYING THE IMAGES FOR SOME SIDE BANTER THAT SVEN WOULDN'T GET
cv2.imshow('frame', frame)
cv2.imshow('red', maskred)
cv2.imshow('blue', maskblue)
cv2.imshow('green', maskgreen) 

cv2.waitKey(0)
cv2.destroyAllWindows()
