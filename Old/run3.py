import cv2 
import numpy as np 
import csv
import pytesseract
import difflib
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
frame=cv2.imread("alf3.jpg")
grapesraw=["Merlot","Grenache","Ugni blanc","Syrah","Carignan","Cabernet Sauvignon","Chardonnay","Cabernet Franc","Gamay","Pinot noir","Sauvignon blanc","Cinsaut","Melon de Bourgogne","Sémillon","Pinot Meunier","Chenin blanc","Mourvèdre","Colombard","Muscat Blanc à Petits Grains","Malbec","Alicante Bouschet","Grenache blanc","Viognier","Muscat de Hambourg","Riesling","Vermentino","Aramon","Gewurztraminer","Tannat","Gros Manseng","Macabeu","Muscat d'Alexandrie","Pinot gris","Clairette","Caladoc","Grolleau","Auxerrois blanc","Marselan","Mauzac","Aligoté","Folle blanche","Grenache gris","Chasselas","Nielluccio","Fer","Muscadelle","Terret blanc","Sylvaner","Piquepoul blanc","Villard noir","Marsanne","Négrette","Roussanne","Pinot blanc","Plantet","Jacquère"]
grapes=[]
for i in grapesraw:
    grapes.append(i.lower())
# FILTERING THE IMAGE
# It converts the BGR color space of image to HSV color space
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

# thresholds for filtering out the random colours
lower_green = np.array([40, 30, 30]) 
upper_green = np.array([80, 255, 255]) 
lower_green = np.array([30, 0, 0]) 
upper_green = np.array([80, 255, 255])
# filtering the image for colours
mask = cv2.inRange(hsv, lower_green, upper_green)
mask=cv2.bitwise_not(mask)
text=pytesseract.image_to_string(mask)
cv2.imwrite("masksven.jpg",mask)
print(text)
lines=text.splitlines()
guesses=[]
for i in lines:
    if len(i)>1:
        match=difflib.get_close_matches(i.lower(),grapes,1,0.65)
        if len(match)>0:
            if difflib.SequenceMatcher(None, i.lower(), match[0]).ratio()>0.9:
                print(match[0])
            else:
                print("it could be ",match[0]," but it's dubious as it has a score of ",difflib.SequenceMatcher(None, i.lower(), match[0]).ratio())
            guesses.append(match[0])
        else:
            print("I'd go with this being wrong")
            guesses.append("")
answers=["merlot","pinot noir","sauvignon blanc","gamay","riesling"]
score=0
print(guesses)
for i in range(5):
    if guesses[i]==answers[i]:
        print("correct")
        score+=1
    else:
        print("WRONG!!!")
print(score)
cv2.imshow('mask', mask)


cv2.waitKey(0)
cv2.destroyAllWindows()
