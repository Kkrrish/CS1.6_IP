import cv2.cv as cv
import cv2
import numpy as np

#read image as grayscale(Hough needs a single channel image)
j=cv2.imread('WithCoins.jpg',0)
j=cv2.medianBlur(j,5)
centrej=cv2.cvtColor(j,cv2.COLOR_GRAY2RGB)

#find circles using the Hough Transform
circles=cv2.HoughCircles(j,cv.CV_HOUGH_GRADIENT,1,5,param1=100,param2=15,minRadius=7,maxRadius=10)
circles=np.uint16(np.around(circles))
circlesW=[]
circlesB=[]

#show circles in green and centres in red
#also classify coins based on the colors at their centres(values by impixel(i) calibration)
for i in circles[0, :] :
	cv2.circle(centrej,(i[0],i[1]),i[2],(0,255,0),2)
	cv2.circle(centrej,(i[0],i[1]),2,(0,0,255),3)
	if j[i[1],i[0]]>120 and j[i[1],i[0]]<160 :
		circlesW.append((i[1],i[0]))
	elif j[i[1],i[0]]>45 and j[i[1],i[0]]<90 :
		circlesB.append((i[1],i[0]))
cv2.imshow('Detected circles and centres',centrej)
cv2.waitKey(0)
cv2.destroyAllWindows()

print circlesW
print circlesB

#show the coin classification(red for white, blue for black)
for i in circlesW :
	cv2.circle(centrej,(i[1],i[0]),2,(0,0,255),3)
for i in circlesB :
	cv2.circle(centrej,(i[1],i[0]),2,(255,0,0),3)
cv2.imshow('Classified circles',centrej)
cv2.waitKey(0)
cv2.destroyAllWindows()
#sweg bitches!