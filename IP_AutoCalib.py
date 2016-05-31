import cv2.cv as cv
import cv2
import numpy as np

#color range constants
maxB=0
minB=0
maxW=0
minW=0

#read image as grayscale(Hough needs a single channel image)
#j is grayscale, p is color
j=cv2.imread('WithCoins.jpg',0)
p=cv2.imread('WithCoins.jpg',-1)
#p=cv2.cvtColor(p,cv2.COLOR_RGB2HSV)
j=cv2.medianBlur(j,5)
centrej=cv2.cvtColor(j,cv2.COLOR_GRAY2RGB)

#global variables to store colors(b,g,r)
#colors for function and colorRed, colorBlack, colorWhite for individual storage
colors=[]
colorRed=[]
colorBlack=[]
colorWhite=[]
rangeRedEnd=[[0,0,0],[0,0,0]]

#global for coords of pockets
pockets=[]

#mouse callback functions, for pockets, red/color and BW
def get_values(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		colors.append([p[y,x,0],p[y,x,1],p[y,x,2]])

def get_values_BW(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		colors.append(j[y,x])

def get_coords(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		pockets.append([y,x])

#for creating a window, binding the function to it, and showing the image in it
def show_Window(purpose):
	cv2.namedWindow(purpose)
	cv2.setMouseCallback(purpose,get_values)
	#show the required image(p) in the window
	while(1):
		cv2.imshow(purpose,p)
		if cv2.waitKey(20) & 0xFF == 27 :
			break
	cv2.destroyAllWindows()

def show_Window_BW(purpose):
	cv2.namedWindow(purpose)
	cv2.setMouseCallback(purpose,get_values_BW)
	#show the required image(p) in the window
	while(1):
		cv2.imshow(purpose,p)
		if cv2.waitKey(20) & 0xFF == 27 :
			break
	cv2.destroyAllWindows()

def show_Window_coords(purpose):
	cv2.namedWindow(purpose)
	cv2.setMouseCallback(purpose,get_coords)
	#show the required image(p) in the window
	while(1):
		cv2.imshow(purpose,p)
		if cv2.waitKey(20) & 0xFF == 27 :
			break
	cv2.destroyAllWindows()

#calculating ranges for red, black, white in b, r, g
def calc_Range(array):
	big=0
	small=0
	for a in range(0,len(array[0])) :
		big=array[0][a]
		small=array[0][a]
		for b in range(0, len(array)) :
			big=max(big,array[b][a])
			small=min(small,array[b][a])
		#return [big,small]
		rangeRedEnd[0][a]+=big+0.8*(big-small)
		rangeRedEnd[1][a]+=small-0.8*(big-small)

def calc_Range_BW(array):
	big=array[0]
	small=array[0]
	for a in range(0,len(array)) :
		big=max(big,array[a])
		small=min(small,array[a])
	return [big+0.8*(big-small),small-0.8*(big-small)]

#read coordinates of pockets
show_Window_coords('Click on all pockets')
print pockets

#read red, black and white colour arrays(b,g,r)
show_Window('Click on all red ends')
colorRed=colors
print colorRed
colors=[]
show_Window_BW('Click on all black coins')
colorBlack=colors
print colorBlack
colors=[]
show_Window_BW('Click on all white coins')
colorWhite=colors
print colorWhite
colors=[]

#alculating and displaying ranges of red ends, and black white coins
calc_Range(colorRed)
print rangeRedEnd
rangeB=calc_Range_BW(colorBlack)
print rangeB
rangeW=calc_Range_BW(colorWhite)
print rangeW

#find circles using the Hough Transform
circles=cv2.HoughCircles(j,cv.CV_HOUGH_GRADIENT,1,5,param1=100,param2=15,minRadius=7,maxRadius=10)
circles=np.uint16(np.around(circles))
circlesW=[]
circlesB=[]
redEnds=[]

#show circles in green and centres in red
#also classify coins based on the colors at their centres(values by impixel(i) calibration)
for i in circles[0, :] :
	cv2.circle(centrej,(i[0],i[1]),i[2],(0,255,0),2)
	cv2.circle(centrej,(i[0],i[1]),2,(0,0,255),3)
	if p[i[1],i[0],2]>rangeRedEnd[1][2] and p[i[1],i[0],2]<rangeRedEnd[0][2] and p[i[1],i[0],1]>rangeRedEnd[1][1] and p[i[1],i[0],1]<rangeRedEnd[0][1] and p[i[1],i[0],0]>rangeRedEnd[1][0] and p[i[1],i[0],0]<rangeRedEnd[0][0] :
		redEnds.append([i[0],i[1]])
	elif j[i[1],i[0]]>rangeW[1] and j[i[1],i[0]]<rangeW[0] :
		circlesW.append([i[1],i[0]])
	elif j[i[1],i[0]]>rangeB[1] and j[i[1],i[0]]<rangeB[0] :
		circlesB.append([i[1],i[0]])
cv2.imshow('Detected circles and centres',centrej)
cv2.waitKey(0)
cv2.destroyAllWindows()

print circlesW
print circlesB

#show the coin classification(red for white, blue for black and unclassified remain red)
for i in circlesW :
	cv2.circle(centrej,(i[1],i[0]),2,(0,255,0),3)
for i in circlesB :
	cv2.circle(centrej,(i[1],i[0]),2,(255,0,0),3)
cv2.imshow('Classified circles',centrej)
cv2.waitKey(0)
cv2.destroyAllWindows()
#sweg bitches!