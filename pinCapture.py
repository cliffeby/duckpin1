import cv2, time
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import style

def distance(ptA, ptB):
    a= ptA[0]-ptB[0]
    b= ptA[1]-ptB[1]
    c= a*a + b*b 
    d = math.sqrt(c)
    return d


def checkOverWrite(pt):
    global pointsDetected
    if len(pointsDetected) <1:
        pointsDetected.append(pt)
        return True
    # print ('OVERWRITE PT DETECTED', pointsDetected, pt)
    for index, ptD in enumerate(pointsDetected):
        # print ('PTDINDEX', ptD[0], ptD[1]) 
        if distance(pt,ptD) < 40:
            return False
        #pointsDetected = []
    pointsDetected.append(pt)
    # print ('TRUE', pt,distance(pt,ptD), len(pointsDetected))
    return True

# Template matching returns two arrays in the 'loc' variable.  The following
# # line is a sample from print(loc)
# # loc =(array([100, 200, 300, 400, 374, 374, 374], dtype=int32), array([10, 20, 30, 40, 302, 303, 304], dtype=int32))
# # Run the following code to understand - for pt in zip(*loc[::-1]): 

# import numpy as np
# loc =(([100, 200, 300, 400, 374, 374, 374]), ([10, 20, 30, 40, 302, 303, 304]))
# print (loc)
# print (loc[::-1])
# print (*loc[::-1])
# for pt in zip(*loc[::-1]):      
#     print (pt)


for x in range(0, 100):
    pointsDetected = []
    img_rgb = cv2.imread("P:/images/image112917" +str(x) +".jpg")

    crop_img = img_rgb[150:750, 200:1000] # Crop from x, y, w, h -> 100, 200, 300, 400
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    img_rgb = crop_img

    # color mask to get red band on pins
    # define the list of boundaries
    boundaries = [([10, 10, 85], [60, 60, 225])]
        # loop over the boundaries
    for (lower, upper) in boundaries:
            # create NumPy arrays from the boundaries
            lower1 = np.array(lower, dtype = "uint8")
            upper1 = np.array(upper, dtype = "uint8")
        
    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(img_rgb, lower1, upper1)
    output = cv2.bitwise_and(img_rgb, img_rgb, mask = mask)
    img_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    template = cv2.imread('P:/images/redBand.jpg',0)
    w, h = template.shape[::-1]

    # res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    # res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF)
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCORR_NORMED)
    # res = cv2.matchTemplate(img_gray,template,cv2.TM_CCORR_)
    threshold = 0.6
    loc = np.where(res >= threshold)
    ptsDetected = []
    for pt in zip(*loc[::-1]):
        
        response = checkOverWrite(pt)
        
        if response:
            # print ("object detected: {}".format(str(pt)), loc)
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
            ptsDetected.append(pt)
            plt.scatter(loc[1],loc[0], label = '.')
            
    next
    plt.show()
    print ('Pins', ptsDetected)


    # pinNames = {'1': 0b1000000000, '2' : 0b0100000000, '3': 0b0010000000, '4': 0b0001000000}
    # for pin in p:
    #     if pin[1] < 50:
    #             pinBin[1,0] = pinNames.get('10', 'default')
    #     if pin[1] > 50 & pin[1] < 100: 
    # next
    # print ("PinBin", pinBin)

    cv2.imshow('Detected'+str(x), img_rgb)
    cv2.waitKey(0)
    print ('New Image _____________________________')
