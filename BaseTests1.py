import cv2
import numpy as np
import matplotlib.pyplot as plt
#
# img = cv2.imread('C:/Users/cliff/PycharmProjects/pinDetect/image1.jpg', cv2.IMREAD_GRAYSCALE)
#img = cv2.imread('C:/Users/cliff/PycharmProjects/pinDetect/image1.jpg', cv2.COLOR_BGR2GRAY)
# img = cv2.imread('C:/Users/cliff/PycharmProjects/pinDetect/image1.jpg', cv2.IMREAD_COLOR)

img = cv2.imread('P:/images/image1129173.jpg')
# img = cv2.imread('C:/Users/cliff/PycharmProjects/pinDetect/image2f.jpg')
# img[y,x]
# img = img[550:2200, 225:650]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.show() 


# Good pin outline
# lower_red = np.array([0,0,0])
# upper_red = np.array([180,255,150])
# Good red collar
# lower_red = np.array([0,100,0])
# upper_red = np.array([180,255,255])

# lower_red = np.array([39,150,0])
# upper_red = np.array([70,255,255])

lower_red = np.array([0,0,100])
upper_red = np.array([110,110,255])

mask =cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imwrite('res2f.jpg',res)

cv2.imshow('image', img)
cv2.imshow('res', res)
cv2.waitKey(0)
cv2.destroyAllWindows