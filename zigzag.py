import cv2
import pyautogui
import numpy as np
import time 
import math

def find_circle(frame):
    frame_gray =  cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray,(9,9),1)
    _ , thresh= cv2.threshold(frame_blur,75,255,cv2.THRESH_BINARY_INV)
    x,y = 0,0
    contours, _ =  cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours :
        if cv2.contourArea(contour)>200 and cv2.contourArea(contour)<400:

            hull = cv2.convexHull(contour)
            (x , y) , r =cv2.minEnclosingCircle(hull)

            x ,y = np.mean(contour,axis=0)[0].astype(int)
            cv2.circle(frame, (x, y), int(r), (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

            cv2.circle(thresh, (x, y), int(r), (255, 255, 255), -1)

    cv2.imshow("frame",frame)
    cv2.imshow("thresh",thresh)
    cv2.waitKey(1)
    return x ,y

    # return None,None


# def find_circle(frame):
#     frame_gray =  cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
#     frame_blur = cv2.GaussianBlur(frame_gray,(5,5),1)
#     circles = cv2.HoughCircles(frame_blur,cv2.HOUGH_GRADIENT,1,40,param1=100,param2=45,minRadius=10,maxRadius=40)
#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         for i in circles[0, :]:
#             x, y, r = i[0],i[1],i[2]
#             if x is not None and y is not None:
#                 cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
#                 cv2.imshow("frame",frame)
#                 cv2.waitKey(1)
#                 return x,y
#     return None,None


def way_detection(frame):
    frame_gray =  cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray,(3,3),1)
    frame_canny = cv2.Canny(frame_blur, 20,100)
    kernel = np.ones((5, 5), np.uint8)
    frame_dilate = cv2.dilate(frame_canny,kernel,iterations=2)
    lines = cv2.HoughLinesP(frame_dilate,1,np.pi/180,50,minLineLength=20,maxLineGap=5)
    if lines is not None:
        for line in lines :
            x1,y1,x2,y2 = line
            angle = math.degrees(math.atan2(y2-y1, x2-x1))
            if 20<angle<50 :
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            elif -50<angle<-20:
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow("thresh",frame_dilate)
    cv2.waitKey(1)
    return lines


def check_direction(x,y,direction,frame,lines):
    #error
    x_new = None
    y_new = None
    for line in lines :
        x1,y1,x2,y2 = line
        angle = math.degrees(math.atan2(y2-y1, x2-x1))

        if  direction =="top_right" and 20<angle<50 :
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        elif direction== "top_left" and -50<angle<-20:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        else:
            continue


        m = (y2-y1)/(x2-x1)
        b1 = y1 - m*x1     
        b2 = y + m*x   

        x_new = int((b2 - b1) / (2 * m))
        y_new = int(m * x_new + b1)

        cv2.line(frame, (x, y), (x_new, y_new), (0, 0, 255), 2)
        cv2.imshow("new_frame",frame)
        cv2.waitKey(1)
    return x_new , y_new


    



def run_game():
    
    pyautogui.sleep(5)
    screen = pyautogui.screenshot()
    screen = np.array(screen)
    # roi= cv2.selectROI('Frame', screen,False)
    #853 374 494 204
    # cv2.destroyWindow('Frame')

    default_direction = "top_right"

    while(True):

        new_frame = pyautogui.screenshot(region=(853,374, 494, 204))
        new_frame = np.array(new_frame)
        new_frame = cv2.cvtColor(new_frame,cv2.COLOR_BGR2RGB)
        x, y = find_circle(new_frame)

        # lines = way_detection(new_frame)

        if x is not None and y is not None:
            cv2.circle(new_frame, (x, y), 3, (0, 0, 255), -1)
            # check_direction (x, y,default_direction, new_frame,lines)

run_game()





    

