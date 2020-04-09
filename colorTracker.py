###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: colorTracker.py
###############################################################################
'''
    FUNCTIONALITY:
    - Tracks Multiple colors and bounds objects of that color with a bounding box
    - Identifies center of given object with red dot
    - Uses sockets to send centerX, and centerY or a given colored object over UDP

'''
# Citations:
#   - https://www.instructables.com/id/Color-Detection-and-Tracking-Using-Open-CV-Python/
#   - https://pythontic.com/modules/socket/udp-client-server-example
#   - https://annystudio.com/software/colorpicker/#download
#   colorpicker was used to find good color values of object being tracked

#   -https://realpython.com/intro-to-python-threading/ - see pandas3dTest.py file
#
# TODO:
#   - Clean up code + build reusable classes
#   - Normalize cx,cy vals either in this file or pandas file

import cv2
import numpy as np
import socket


serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)


while True:
    # _ is used to unpack values we don't want to use
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # Yellow - working
    lowerColY = np.array([20, 110, 110,])
    upperColY = np.array([40, 255, 255])
    yelMask = cv2.inRange(hsv, lowerColY, upperColY)


    # Blue - working
    lowerColB = np.array([100, 100, 120])
    upperColB = np.array([126, 255, 255])
    blueMask = cv2.inRange(hsv, lowerColB, upperColB)

    # Green - not done yet
    lowerColG = np.array([65, 60, 60])
    upperColG = np.array([80, 255, 255])
    greenMask = cv2.inRange(hsv, lowerColG, upperColG)

    # Red - not done yet



    # unpacks as two values instead of three because of cv2 versioning
    # finds blue objects
    (contours,_) = cv2.findContours(blueMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 800:
            x,y,w,h = cv2.boundingRect(contour)
            cx = x + (w//2)
            cy = y + (h//2)
            # changed to show center of object
            frame = cv2.rectangle(frame, (cx,cy),(x+w//2, y+h//2), (0,0,255), 10)
            cv2.putText(frame,"Blue color",(x,y),cv2.FONT_HERSHEY_TRIPLEX, 2.0, (255,0,0), 6)

            # prints coordinates of upper-left (x,y)
            # prints coordinates of center (x,y)
            #print('BLUE_ ','UPL-X: ',x, 'UPL-Y: ', y , 'C-X: ', cx, 'C-Y', cy)


    # finds yellow objects
    (contours,_) = cv2.findContours(yelMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 800:
            x,y,w,h = cv2.boundingRect(contour)
            cx = x + (w//2)
            cy = y + (h//2)
            # changed to show center of object
            frame = cv2.rectangle(frame, (cx,cy),(x+w//2, y+h//2), (0,0,255), 10)
            cv2.putText(frame,"Yellow color",(x,y),cv2.FONT_HERSHEY_TRIPLEX, 2.0, (0,255,255), 6)

            # prints coordinates of upper-left (x,y)
            # prints coordinates of center (x,y)
            print('YELLOW_ ','UPL-X: ',x, 'UPL-Y: ', y , 'C-X: ', cx, 'C-Y', cy)
            # converts cx,cy and sends over UDP to panda3D server
            cents = str.encode(f'{cx},{cy}')
            UDPClientSocket.sendto(cents, serverAddressPort)
            print(cx, cy)

    # finds green objects
    (contours,_) = cv2.findContours(greenMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 800:
            x,y,w,h = cv2.boundingRect(contour)
            cx = x + (w//2)
            cy = y + (h//2)
            # changed to show center of object
            frame = cv2.rectangle(frame, (cx,cy),(x+w//2, y+h//2), (0,0,255), 10)
            cv2.putText(frame,"Green color",(x,y),cv2.FONT_HERSHEY_TRIPLEX, 2.0, (0,255,0), 6)

            # prints coordinates of upper-left (x,y)
            # prints coordinates of center (x,y)
            #print('GREEN_ ','UPL-X: ',x, 'UPL-Y: ', y , 'C-X: ', cx, 'C-Y', cy)

    cv2.imshow('tracking', frame)

    #cv2.imshow('c-tracking', cFrame)

    k = cv2.waitKey(5) & 0XFF
    if k == 27:
        break

    #green = np.uint8([[[0,0,255 ]]])
    #hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    #print(hsv_green)

cv2.destroyAllWindows()
cap.release()
