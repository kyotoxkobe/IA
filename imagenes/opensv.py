import cv2 as cv
img = cv.imread('img/manzana.jpg',1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# cv.imshow('Original', img)

ubb = (0,60,60)
uba = (10,255,255)
ubb1 = (170,60,60)
uba1 = (180,255,255)
    
mask = cv.inRange(hsv, ubb, uba)
mask1 = cv.inRange(hsv, ubb1, uba1)
mask = mask + mask1
result = cv.bitwise_and(img, img, mask=mask)
cv.imshow('Result', result)
cv.imshow('Mask', mask)
cv.imshow('Mask1', mask1)
cv.imshow('Original', img)
cv.imshow('Gray', img2)
cv.imshow('HSV', hsv)
cv.waitKey(0)
cv.destroyAllWindows()
