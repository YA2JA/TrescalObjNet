import cv2

from settings import *
from PILs import join_white_space, join_images

stop = False
freeze = False

def back(event, x, y, flags, param):
    global stop, freeze

    if event == cv2.EVENT_LBUTTONDOWN:
        if ( 25 < x < 125) and (500 < y < 550):
            stop = True

        if ( 145 < x < 245) and (500 < y < 550):
            freeze = not freeze

def draw_buttons(window):
    x, y = 25, 500
    w, h = 100, 50
    cv2.rectangle(window, (x, y), (x+w, y+h),  (255, 0, 0), 5)
    cv2.putText(window, 'Stop', (x+13, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    x, y = 145, 500
    w, h = 120, 50
    cv2.rectangle(window, (x, y), (x+w, y+h),  (255, 0, 0), 5)
    cv2.putText(window, 'Freeze', (x+10, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

def draw_interface(window, output):
    window = join_white_space(window)
    output = join_white_space(output)
    window = join_images(window, output)
    
    draw_buttons(window)
    cv2.imshow('frame', window)
    cv2.resizeWindow("frame", 720, 600)
    cv2.setMouseCallback("frame", back)
    
    if cv2.waitKey(1) == ord('q') or stop:
        raise KeyError ("Application has been stopped")
    return freeze