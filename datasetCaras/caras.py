import numpy as np
import cv2 as cv
import math 
import os

rostro = cv.CascadeClassifier('/home/julian/Documentos/IA/datasetCaras/Haarcascade/haarcascade_frontalface_alt2.xml')

# Verificar que el clasificador se cargó correctamente
if rostro.empty():
    print("Error: No se pudo cargar el clasificador Haar")
    exit()

# Crear el directorio si no existe
output_dir = '/home/julian/Documentos/IA/datasetCaras/Haarcascade/fotos/julian'
os.makedirs(output_dir, exist_ok=True)

cap = cv.VideoCapture(0)
i = 0  
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: No se pudo capturar el frame")
        break
        
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    
    # Variable para mostrar solo un rostro por frame
    rostro_detectado = None
    
    for(x, y, w, h) in rostros:
       # Dibujar rectángulo alrededor del rostro
       frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
       frame2 = frame[y:y+h, x:x+w]
       
       frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)
       
       if(i%5==0):
           filename = os.path.join(output_dir, f'julian{i}.jpg')
           cv.imwrite(filename, frame2)
           print(f"Imagen guardada: {filename}")
       
       # Guardar solo el primer rostro detectado para mostrar
       if rostro_detectado is None:
           rostro_detectado = frame2
           
    # Mostrar solo una ventana del rostro si se detectó alguno
    if rostro_detectado is not None:
        cv.imshow('rostro', rostro_detectado)
    
    cv.imshow('rostros', frame)
    i = i+1
    k = cv.waitKey(1) & 0xFF
    if k == 27:  # ESC para salir
        break

cap.release()
cv.destroyAllWindows()