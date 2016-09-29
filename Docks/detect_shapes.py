# import shit
from shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# construct argument parse and parse said arguement
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, 
	help = "path to the input image")
args = vars(ap.parse_args())

# load the image and resize it
image = cv2.imread(args["image"])
resized = imutils.resize(image, width = 300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur, and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]

# find contours in thresholded image and initialize shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# loop over contours
for c in cnts:
	# compute center, detect name of shape
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and nape of the shapes
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 
		0.5, (255, 255, 255), 2)

# show image
cv2.imshow("Image", image)
cv2.waitKey(0)