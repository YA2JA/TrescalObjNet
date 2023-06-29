import cv2

from CVs import pre_process, post_process_crop, post_process_image_to_text
from settings import SCREEN_NET, DIGITS_NET
from PILs import get_error_image
from interface import draw_interface


def resize(image, width):
    height = int(image.shape[1] * width / image.shape[0])
    return cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

def get_screen(frame):
    try:
        net = pre_process(frame.copy(), SCREEN_NET, 640, 640)
        screen_img = post_process_crop(frame.copy(), net, 640, 640)
        return resize(screen_img, 360)
    except:
        return get_error_image()

def get_digits(frame):
    net = pre_process(frame.copy(), DIGITS_NET, 640, 640)
    digits, message = post_process_image_to_text(frame.copy(), net, 640, 640)
    print(message)
    return digits

def main():
    cam = cv2.VideoCapture(0)
    freeze = False
    
    while True:
        ret, frame = cam.read()

        if not freeze:
            screen_image = get_screen(frame)
            output = get_digits(screen_image)
        freeze = draw_interface(frame, output)



if __name__ == '__main__':
    main()