from PIL import Image, ImageFont, ImageDraw

import numpy as np
import cv2

BLACK = (0,0,0)

def toImgOpenCV(imgPIL): 
      # Conver imgPIL to imgOpenCV
      i = np.array(imgPIL)

      #Here I swap R with B arrays
      # After mapping from PIL to numpy : [R,G,B,A]
      # numpy Image Channel system: [B,G,R,A]
      i[:,:,0], i[:,:,2] = i[:,:,2].copy(), i[:,:,0].copy()
      return i

def join_images(in_1, in_2):
      image_1 = Image.fromarray(cv2.cvtColor(in_1, cv2.COLOR_BGR2RGB))
      image_2 = Image.fromarray(cv2.cvtColor(in_2, cv2.COLOR_BGR2RGB))

      width = image_1.size[0] + image_2.size[0]
      height = image_1.size[0] if image_1.size[1]  > image_2.size[1] else image_2.size[1]

      image = Image.new("RGB", (width, height))
      image.paste(image_1, (0, 0))
      image.paste(image_2, (image_1.size[0], 0))

      return toImgOpenCV(image)

def join_white_space(in_1, target_size = 600):
    image_1 = Image.fromarray(cv2.cvtColor(in_1, cv2.COLOR_BGR2RGB))
    white_space = Image.new("RGB", (360, 600 - image_1.size[1]), (255, 255, 255))
    
    image = Image.new("RGB", (360, 600))
    image.paste(image_1, (0, 0))
    image.paste(white_space, (0, image_1.size[1]))
    
    return toImgOpenCV(image)
    
def get_error_image(message="Multimeter\nNot found"):
    error_message = Image.new("RGB", (360, 360), (255, 255, 255))
    fnt = ImageFont.truetype("arial.ttf", 40)
    draw = ImageDraw.Draw(error_message)
    draw.text((30, 30), message, font=fnt, fill=BLACK)
    output = toImgOpenCV(error_message)
    return output

def crop(image, left, top, width, height):
    return toImgOpenCV(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).crop((left, top, left + width, top + height)))

def resize_prop(image, width, height):
    
    image = image = image.resize(width, height)