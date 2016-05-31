import cv2.cv as cv
import cv2
import numpy as np

#color range constants
maxB=0
minB=0
maxW=0
minW=0

cap = cv2.VideoCapture(0)

# Capture frame-by-frame
ret, p = cap.read()
j=cv2.cvtColor(p,cv2.COLOR_BGR2GRAY)
#read image as grayscale(Hough needs a single channel image)
#j is grayscale, p is color(RGB), q is color(HSV)
#j=cv2.imread('WithCoins.jpg',0)
#p=cv2.imread('WithCoins.jpg',-1)
q=cv2.cvtColor(p,cv2.COLOR_RGB2HSV)
q=cv2.medianBlur(q,7)
j=cv2.medianBlur(j,5)
centrej=cv2.cvtColor(j,cv2.COLOR_GRAY2RGB)

cv2.imshow('Our image in HSV',q)
cv2.waitKey(0)
cv2.destroyAllWindows()

#global variables to store colors(b,g,r)
#colors for function and colorRed, colorBlack, colorWhite for individual storage
colors=[]
colorRed=[]
colorBlack=[]
colorWhite=[]
rangeRedEnd=[[0,0],[0,0]]
rangeBW=[[0,0],[0,0]]
rangeB=[[0,0],[0,0]]

#global for coords of pockets
pockets=[]

#mouse callback functions, for pockets, red/color and BW
def get_values(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		colors.append([q[y,x,0],q[y,x,1],q[y,x,2]])

#def get_values_BW(event,x,y,flags,param):
#	if event == cv2.EVENT_LBUTTONDOWN:
#		colors.append(j[y,x])

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

def show_Window_coords(purpose):
	cv2.namedWindow(purpose)
	cv2.setMouseCallback(purpose,get_coords)
	#show the required image(p) in the window
	while(1):
		cv2.imshow(purpose,p)
		if cv2.waitKey(20) & 0xFF == 27 :
			break
	cv2.destroyAllWindows()

#calculating ranges for red, black, white in H and S
def calc_Range(array):
	big=0
	small=0
	for a in range(0,len(array[0])-1) :
		big=array[0][a]
		small=array[0][a]
		for b in range(0, len(array)) :
			big=max(big,array[b][a])
			small=min(small,array[b][a])
		rangeRedEnd[0][a]+=big+0.8*(big-small)
		rangeRedEnd[1][a]+=small-0.8*(big-small)

def calc_Range_BW(array):
	big=0
	small=0
	for a in range(0,len(array[0])-1) :
		big=array[0][a]
		small=array[0][a]
		for b in range(0, len(array)) :
			big=max(big,array[b][a])
			small=min(small,array[b][a])
		rangeBW[0][a]+=big+0.8*(big-small)
		rangeBW[1][a]+=small-0.8*(big-small)


#read coordinates of pockets
show_Window_coords('Click on all pockets')
print pockets

#read red, black and white colour arrays(b,g,r)
show_Window('Click on all the red ends')
colorRed=colors
print colorRed
colors=[]
show_Window('Click on all the black coins')
colorBlack=colors
print colorBlack
colors=[]
show_Window('Click on all the white coins')
colorWhite=colors
print colorWhite
colors=[]

#alculating and displaying ranges of red ends, and black white coins
calc_Range(colorRed)
print rangeRedEnd
calc_Range_BW(colorBlack)
rangeB=rangeBW
print rangeBW
rangeBW=[[0,0],[0,0]]
calc_Range_BW(colorWhite)
print rangeBW

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
	if q[i[1],i[0],1]>rangeRedEnd[1][1] and q[i[1],i[0],1]<rangeRedEnd[0][1] and q[i[1],i[0],0]>rangeRedEnd[1][0] and q[i[1],i[0],0]<rangeRedEnd[0][0] :
		redEnds.append([i[0],i[1]])
	elif q[i[1],i[0],1]>rangeBW[1][1] and q[i[1],i[0],1]<rangeBW[0][1] and q[i[1],i[0],0]>rangeBW[1][0] and q[i[1],i[0],0]<rangeBW[0][0] :
		circlesW.append([i[1],i[0]])
	elif q[i[1],i[0],1]>rangeB[1][1] and q[i[1],i[0],1]<rangeB[0][1] and q[i[1],i[0],0]>rangeB[1][0] and q[i[1],i[0],0]<rangeB[0][0] :
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
cv2.imshow('Classified circles(Red are unclassified)',centrej)
cv2.waitKey(0)
cv2.destroyAllWindows()
#sweg bitches!