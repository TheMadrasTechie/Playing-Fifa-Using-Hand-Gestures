from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import key_press as kp

cap = cv2.VideoCapture(0)
#def move(x,y,):
    #if() 
greenLower = (44, 100, 100)
greenUpper = (64, 255, 255)
blueLower = (110, 100, 100)
blueUpper = (130, 255, 255)
redLower = (-10, 100, 100)
redUpper = (10, 130, 130)
pinkLower = (155, 100, 100)
pinkUpper = (175, 255, 255)
yellowLower = (20, 100, 100)
yellowUpper = (40, 255, 255) 

font = cv2.FONT_HERSHEY_SIMPLEX
#pts = deque(maxlen=args["buffer"])
pts_green = deque(maxlen=64)
pts_blue = deque(maxlen=64)
pts_red = deque(maxlen=64)
pts_pink = deque(maxlen=64)
pts_yellow = deque(maxlen=64)
o=0
def passs(btn):
    if(btn=='d'):
        kp.PressKey(0x20)
        time.sleep(.2)
        kp.ReleaseKey(0x20)
    elif(btn=='g'):        
        kp.PressKey(0x39)
        time.sleep(.2)
        kp.ReleaseKey(0x39)  
def move (pts):
  if((pts[0] is not None)and(pts[1] is not None)):  
    #kp.PressKey(0x12)
    x=pts[0][0]-pts[1][0]
    y=pts[0][1]-pts[1][1]
    if(x>0):
        print("right")
        kp.ReleaseKey(0xCD)
        kp.PressKey(0xCB) 
    elif(x<0)   :
        print("left")
        kp.ReleaseKey(0xCB)
        kp.PressKey(0xCD)
    if(y>0):   
        print("down")
        kp.ReleaseKey(0xC8)
        kp.PressKey(0xD0)
    elif(y<0):
        print("up")    
        kp.ReleaseKey(0xD0)
        kp.PressKey(0xC8)
def release_all():        
    kp.ReleaseKey(0xD0)
    kp.ReleaseKey(0xC8)
    kp.ReleaseKey(0xCD)
    kp.ReleaseKey(0xCB)
while True:
    #release_all()
    frame = cap.read()
    frame = frame[1] 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask_green = cv2.inRange(hsv, greenLower, greenUpper)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)
    cnts_green = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts_green = cnts_green[0] if imutils.is_cv2() else cnts_green[1]
    center = None
    if len(cnts_green) > 0:
        c = max(cnts_green, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
            release_all()
 
    # update the points queue
    
    mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)
    # find contours in the mask_green and initialize the current
    # (x, y) center of the ball
    cnts_blue = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts_blue = cnts_blue[0] if imutils.is_cv2() else cnts_blue[1]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts_blue) > 0:
        # find the largest contour in the mask_green, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts_blue, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.putText(frame, "Blue", (int(x-2), int(y-2)), font, 0.8, (255,0,0), 2, cv2.LINE_AA)
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (255, 0, 0), 2)
            cv2.circle(frame, center, 5, (255, 0, 0), -1)
        move(pts_blue)
    # update the points queue
    pts_blue.appendleft(center)
        # loop over the set of tracked points
    for i in range(1, len(pts_blue)):
        # if either of the tracked points are None, ignore
        # them
        if pts_blue[i - 1] is None or pts_blue[i] is None:
            continue
 
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        o=o+1
        #print("Virus Attack in Your Computer \t Virus Number"+str(o))
        #print("You will get a video called Virus")
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame, pts_blue[i - 1], pts_blue[i], (255, 0,0 ), thickness)
 
    # update the points queue
    

    mask_red = cv2.inRange(hsv, redLower, redUpper)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.dilate(mask_red, None, iterations=2)
    # find contours in the mask_green and initialize the current
    # (x, y) center of the ball
    cnts_red = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts_red = cnts_red[0] if imutils.is_cv2() else cnts_red[1]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts_red) > 0:
        # find the largest contour in the mask_green, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts_red, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
    # update the points queue
    
    
    mask_pink = cv2.inRange(hsv, pinkLower, pinkUpper)
    mask_pink = cv2.erode(mask_pink, None, iterations=2)
    mask_pink = cv2.dilate(mask_pink, None, iterations=2)
    # find contours in the mask_green and initialize the current
    # (x, y) center of the ball
    cnts_pink = cv2.findContours(mask_pink.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts_pink = cnts_pink[0] if imutils.is_cv2() else cnts_pink[1]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts_pink) > 0:
        # find the largest contour in the mask_green, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts_pink, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, center, 5, (0, 110, 255), -1)
            passs('d')
 
    
    mask_yellow = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
    mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)
    cnts_yellow = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts_yellow = cnts_yellow[0] if imutils.is_cv2() else cnts_yellow[1]
    center = None
    if len(cnts_yellow) > 0:
        c = max(cnts_yellow, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            passs('g')
            cv2.circle(frame, center, 5, (0, 255, 255), -1)
    
    dd = cv2.flip(frame, 1)
    dd = cv2.resize(dd, (500,dd.shape[0]), interpolation = cv2.INTER_AREA)
    cv2.imshow("Ball", dd)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()