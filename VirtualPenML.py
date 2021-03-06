import cv2
import numpy as np

try:
    cap.release()
except:
    pass
import time

cap = cv2.VideoCapture(0)
kernel = np.ones((5, 5), np.uint8)
cv2.namedWindow('image2', cv2.WINDOW_NORMAL)
canvas = None
pt1, pt2 = 0, 0
clear = False
while (1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([26, 80, 147])
    upper_red = np.array([81, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        area = cv2.contourArea(c)

        if pt1 == 0 and pt2 == 0:
            pt1, pt2 = x, y
        else:
            canvas = cv2.line(canvas, (pt1, pt2), (x, y), [0, 255, 0], 2)
        pt1, pt2 = x, y

        if area > 50000:
            cv2.putText(canvas, 'Clearing Canvas', (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
            clear = True
    # print(area)
    else:
        pt1, pt2 = 0, 0

    # print(frame.shape,mask.shape)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # print(res.shape)
    frame = cv2.add(frame, canvas)
    cv2.imshow('image2', frame)
    # cv2.imshow('mask',mask)
    if clear == True:
        time.sleep(0.8)
        canvas = np.zeros_like(frame)
        clear = False

    # cv2.imshow('res',res)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()