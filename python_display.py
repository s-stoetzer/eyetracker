# -*- coding: utf-

# import openCV
import cv2
#is not used in the example, but makes sense for further experiments...
import numpy as np

# use first video device (USB); if there are several cameras, select the correct number.
cap = cv2.VideoCapture(3)

while True:

    video = False # wait for frame from USB device
    while video == False:
        video, frame = cap.read() # keep reading until we get a frame

    # now we can search for the pupil... there are different ways to do it
    # 2 examples:   use binary conversation, check for black spot (iris)
    #               search for circular structures of the right size

    #flip retrieves frame, it is rotated 180°
    (h, w) = frame.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    frame = cv2.warpAffine(frame, M, (w, h))

    #convert to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    #apply a gaussian filter, removing noise
    blur = cv2.medianBlur(gray, 5)

    #apply adaptive bightness correction
    cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
    clahe = cl1.apply(blur)

    # find iris by black/white conversion --> only exmaple image, no further processing
    (thresh, iris) = cv2.threshold(clahe, 50, 255, cv2.THRESH_BINARY)

    #find circular structures with radi between 10 and 30
    circles = cv2.HoughCircles(clahe ,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=40)

    #only check if any circles have been found
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int") #convert float to integer
        print ('integer',circles) #print the radi for adjustment
        # mark all circular structures in the received frame
        for (x,y,r) in circles:
            cv2.circle(frame, (x, y), r, (0, 0, 255), 2)

    cv2.imshow('Frame', frame) #retieved original image with circules marked
    cv2.imshow('Auge', iris) #show black and white conversion; iris=black spot
    cv2.imshow('Clahe', clahe) #
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
