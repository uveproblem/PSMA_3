import cv2
import numpy as np
#import numpy as np

webcam = cv2.VideoCapture(0)
while True:
    _, frame = webcam.read()
    frame = cv2.flip(frame, 1)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #RED
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    #GREEN
    green_lower = np.array([20, 62, 30], np.uint8)
    green_upper = np.array([40, 75, 65], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    #BLUE
    blue_lower = np.array([0, 0, 255], np.uint8)
    blue_upper = np.array([180, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
    #KERNAL
    kernal = np.ones((5, 5), np.uint8)
    green_mask = cv2.dilate(green_mask, kernal)
    #CONTOUR_GREEN
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 200:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.putText(frame, "Green", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #CONTOUR_BLUE
    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 200:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (225, 0, 0), 5)
            cv2.putText(frame, "blue", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), 2)
    #CONTOUR_RED
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 200:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 225), 5)
            cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)
    #IM_SHOW
    #cv2.imshow('frame', frame)
    #cv2.imshow('red_mask', red_mask)
    #cv2.imshow('green_mask', green_mask)
    #cv2.imshow('blue_mask', blue_mask)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(20)
    if key == ord('q'):
        break
