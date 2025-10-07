import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

# Crear canvas negro para la estela
trail = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if trail is None:
        trail = np.zeros_like(frame)  # se inicializa en el primer frame
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # Rangos para el color rojo
    ubb = (0, 60, 60)
    uba = (10, 255, 255)
    ubb1 = (170, 60, 60)
    uba1 = (180, 255, 255)
    
    mask = cv.inRange(hsv, ubb, uba)
    mask1 = cv.inRange(hsv, ubb1, uba1)
    mask = mask + mask1
    
    # Encontrar contornos para localizar el objeto
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if contours:
        # Tomar el contorno más grande (el objeto rojo principal)
        c = max(contours, key=cv.contourArea)
        (x, y, w, h) = cv.boundingRect(c)
        center = (x + w // 2, y + h // 2)
        
        # Dibujar un punto en la estela
        cv.circle(trail, center, 5, (0, 0, 255), -1)
        
        # Dibujar también un rectángulo en el frame actual
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Superponer la estela sobre el frame original
    output = cv.add(frame, trail)

    cv.imshow('Frame', output)
    cv.imshow('Mask', mask)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
