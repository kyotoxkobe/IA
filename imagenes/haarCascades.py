# Haar cascades
import cv2 as cv
import numpy as np

# Descarga los archivos desde las referencias web y colócalos en el directorio actual
rostro = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
ojo = cv.CascadeClassifier('haarcascade_eye.xml')

cap = cv.VideoCapture(0)
x = y = w = h = 0
img = 0
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = rostro.detectMultiScale(gris, 1.3, 5)
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gris[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        ojos = ojo.detectMultiScale(roi_gray)
        for (ox, oy, ow, oh) in ojos:
            cv.rectangle(roi_color, (ox, oy), (ox + ow, oy + oh), (0, 255, 0), 2)
    if w != 0 and h != 0:
        img = frame[y:y + h, x:x + w]
    cv.imshow('Frame', frame)
    k = cv.waitKey(1) & 0xFF
    if k == ord('s'):
        if w != 0 and h != 0:
            count += 1
            cv.imwrite('rostro_{}.png'.format(count), img)
            print("Imagen almacenada")
        else:
            print("No se ha detectado rostro")
    elif k == ord('q'):
        break
cap.release()
cv.destroyAllWindows()