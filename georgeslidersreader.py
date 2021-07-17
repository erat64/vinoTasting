import cv2 
import numpy as np 
import csv
# OPENING THE IMAGE
#cap = cv2.VideoCapture(0) 
frame=cv2.imread("test2.jpg")

# FILTERING THE IMAGE
# It converts the BGR color space of image to HSV color space 
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

# thresholds for filtering out the random colours
lower_red1 = np.array([155, 30, 100])
upper_red1 = np.array([180,255,255])
lower_red2 = np.array([0, 30, 100])
upper_red2 = np.array([25,255,255])
lower_blue = np.array([90, 30, 50]) 
upper_blue = np.array([140, 255, 255]) 

# filtering the image for colours
maska = cv2.inRange(hsv, lower_red1, upper_red1)
maskb = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.add(maska,maskb)
mask2 = cv2.inRange(hsv, lower_blue, upper_blue)

kernel = np.ones((4,4),np.float32)/16
mask = cv2.filter2D(mask,-1,kernel)
mask = cv2.filter2D(mask,-1,kernel)
mask = cv2.filter2D(mask,-1,kernel)
mask = cv2.filter2D(mask,-1,kernel)
mask = cv2.filter2D(mask,-1,kernel)
ret,mask = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)

kernel = np.ones((5,5),np.float32)/25
mask2 = cv2.filter2D(mask2,-1,kernel)
mask2 = cv2.filter2D(mask2,-1,kernel)
ret,mask2 = cv2.threshold(mask2,127,255,cv2.THRESH_BINARY)
# DETECTING THE CENTROIDS
_,img = cv2.threshold(mask,0,255,cv2.THRESH_OTSU)
h, w = img.shape[:2]
centriods, contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
moments  = [cv2.moments(cnt) for cnt in contours0]
# Rounded the centroids to integer.
centroids = [( int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ) for m in moments]
print('centroids:', centroids)
# draw circle to mark the centriod locations
for c in centroids:
        cv2.circle(mask,c,5,(0,0,0))

_,img = cv2.threshold(mask2,0,255,cv2.THRESH_OTSU)
h, w = img.shape[:2]
centriods2, contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
moments  = [cv2.moments(cnt) for cnt in contours0]
# Rounded the centroids to integer.
centroids2 = [( int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ) for m in moments]
print('centroids2:', centroids2)
# draw circle to mark the centriod locations
for c in centroids2:
        cv2.circle(mask2,c,5,(0,0,0))

# PAIRING OFF THE COORDS FROM THE SAME QUESTION
pairs=[]
for i in centroids:
        blues=[]
        for j in centroids2:                
                if i[1]<j[1]+20 and i[1]>j[1]-20:
                        blues.append(j)
        blues.append(i)
        pairs.append(blues)
def distance(x,y):
        total=0
        for i in range(len(x)):
                total+=(x[i]-y[i])**2
        return total**0.5

# WORKING OUT THE SCORES
scores=[]
for i in pairs:
        output=[]
        output.append(distance(i[0],i[2])/(distance(i[0],i[2])+distance(i[1],i[2])))
        output.append((i[0][1]+i[1][1]+i[2][1])/3)
        scores.append(output)

# WRITING THE TO CSV
with open('answers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(scores)#"""

# DISPLAYING THE IMAGES FOR SOME SIDE BANTER THAT SVEN WOULDN'T GET
cv2.imshow('frame', frame)
cv2.imshow('mask', mask)
cv2.imshow('mask2', mask2) 

cv2.waitKey(0)
cv2.destroyAllWindows()
