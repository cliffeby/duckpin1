# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "P:/images/image1129174.jpg")
args = vars(ap.parse_args())
 
# load the image
# image = cv2.imread(args["image"])
for x in range(0, 100):
    image = cv2.imread("P:/images/image112917" +str(x) +".jpg")

    # define the list of boundaries
    boundaries = [
        ([10, 10, 85], [60, 60, 215])
    ]
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower1 = np.array(lower, dtype = "uint8")
        upper1 = np.array(upper, dtype = "uint8")
    
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower1, upper1)
        output = cv2.bitwise_and(image, image, mask = mask)
    
        # show the images
        cv2.imshow("images", np.hstack([image, output]))
        cv2.waitKey(0)