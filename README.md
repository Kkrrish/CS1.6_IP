# CS1.6_IP
My Institute Technical Summer Project required Image Processing for detection and classification of coins on a carrom board.
It uses the Hough Transform for detecting circles(and provides their radii too).

## The Hough Transform:
Thresholding is done first, and then followed by "Edge Detection" as in openCV.
Using the obtained edges, a circle is detected(if it falls within the parameters of the function).
The main(important) parameters are Minimum and Maximum circle Radii and the Minimum possible distance between two circles.

## Additions to core algorithm:
1. Auto-Calibration: User is asked to point to as many similar colored pieces as possible(For each:Red, Black and White coins).
This allows me to calculate range of values of pixels corresponding to that particular colour.
Adds flexibility of environment and lighting condition.(Note: HSV is used for classification/thresholding).

2. Camera Input: You can take input from the default camera of the computer.
This enables you to attach a USB webcam for the purpose of image capture.
It was added primarily due to its requirement in my specific application.

##Algorithm Integration:
The Decision Making Algorithm for the Carrom Playing Bot in our project was developed independently from Image Processing.
The final merged file has been added here. w
It is capable of:
-Image Processing(Coin Detection and Identification)
-Serial Communication with Arduino for shot initiation and motor control
-Shot decision using AI

### Thank you.
