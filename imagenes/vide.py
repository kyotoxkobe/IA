import cv2 as cv

cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    ubb = (0,60,60)
    uba = (10,255,255)
    ubb1 = (170,60,60)
    uba1 = (180,255,255)
    
    mask = cv.inRange(hsv, ubb, uba)
    mask1 = cv.inRange(hsv, ubb1, uba1)
    #mask = mask + mask1
    result = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('HSV', hsv)
    cv.imshow('Frame', frame)
    # cv.imshow('Mask', mask)
    cv.imshow('Result', result)
    # cv.imshow('RGB', rgb) #rgb
    # cv.imshow('Gray', gray) #gris
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()