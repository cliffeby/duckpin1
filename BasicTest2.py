import cv2
import numpy as np
from matplotlib import pyplot as plt
img_rgb = cv2.imread('/home/pi/Shared/images/image2f.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('C:/Users/cliff/OneDrive/images/pattern3Pin.jpg',0)
template = cv2.imread('/home/pi/Shared/images/redBand.jpg',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.95
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
# cv2.imwrite('res.jpg',img_rgb)
cv2.imshow('res.jpg', img_rgb)
cv2.imshow('gray', img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows