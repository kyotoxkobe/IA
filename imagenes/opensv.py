import cv2 as cv
import numpy as np
img = cv.imread('C:\\IA\\IA\\imagenes\\img\\buscar.jpeg',1)
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
resultRed = cv.bitwise_and(img, img, mask=mask)
cv.imshow('Result', resultRed)
#necesito buscar el color azul de la imagen tambien

ubb = (100,150,0)
uba = (140,255,255)

mask = cv.inRange(hsv, ubb, uba)
resultBlue = cv.bitwise_and(img, img, mask=mask)
cv.imshow('Result azul', resultBlue)
# tambien el verde y amarillo

ubb = (40, 40, 40)
uba = (80, 255, 255)

mask = cv.inRange(hsv, ubb, uba)
resultGreen = cv.bitwise_and(img, img, mask=mask)
cv.imshow('Result verde', resultGreen)

ubb = (20, 100, 100)
uba = (30, 255, 255)

mask = cv.inRange(hsv, ubb, uba)
resultYellow = cv.bitwise_and(img, img, mask=mask)
cv.imshow('Resultado amarillo', resultYellow)

# mostrar donde estan los colores en base al centro con coordenadas x,y
# x, y, w, h = cv.boundingRect(mask)
# cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
# cv.imshow('Frame', img)
# Encontrar centro de colores usando solo mascaras sin contornos
#buscar todas las manchas de los diferentes colores y sacar su centro sin usar contornos ni cv.boundingRect 
# Para el color rojo
mask_red = cv.inRange(hsv, (0,60,60), (10,255,255))
mask_red1 = cv.inRange(hsv, (170,60,60), (180,255,255))
mask_red = mask_red + mask_red1
if np.any(mask_red):
    y, x = np.where(mask_red > 0)
    xRojo = int(np.mean(x))
    yRojo = int(np.mean(y))
    print(f"Centro del color rojo: ({xRojo}, {yRojo})")

# Para el color azul
mask_blue = cv.inRange(hsv, (100,150,0), (140,255,255))
if np.any(mask_blue):
    y, x = np.where(mask_blue > 0)
    xAzul = int(np.mean(x))
    yAzul = int(np.mean(y))
    print(f"Centro del color azul: ({xAzul}, {yAzul })")

# Para el color verde
mask_green = cv.inRange(hsv, (40, 40, 40), (80, 255, 255))
if np.any(mask_green):
    y, x = np.where(mask_green > 0)
    xVerde = int(np.mean(x))
    yVerde = int(np.mean(y))
    print(f"Centro del color verde: ({xVerde}, {yVerde})")

# Para el color amarillo
mask_yellow = cv.inRange(hsv, (20, 100, 100), (30, 255, 255))
if np.any(mask_yellow):
    y, x = np.where(mask_yellow > 0)
    xAmarillo = int(np.mean(x))
    yAmarillo = int(np.mean(y))
    print(f"Centro del color amarillo: ({xAmarillo}, {yAmarillo})")














# cv.imshow('Mask', mask)
# cv.imshow('Mask1', mask1)
# cv.imshow('Original', img)
# cv.imshow('Gray', img2)
# cv.imshow('HSV', hsv)
cv.waitKey(0)
cv.destroyAllWindows()


#VIDEO
