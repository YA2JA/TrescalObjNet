import numpy as np

from PILs import crop
from PIL import Image
from settings import *

def pre_process(input_image, net, width, hieght):
      blob = cv2.dnn.blobFromImage(input_image, 1/255,  (width, hieght), [0,0,0], 1, crop=False)
      net.setInput(blob)
      outputs = net.forward(net.getUnconnectedOutLayersNames())
      return outputs


def post_process_crop(input_image, outputs, in_width, in_hieght):
      rows = outputs[0].shape[1]
      image_height, image_width = input_image.shape[:2]
      x_factor = image_width / in_width
      y_factor =  image_height / in_hieght
      
      for r in range(rows):
            row = outputs[0][0][r]
            confidence = row[4]
            if confidence >= CONFIDENCE_THRESHOLD_SCREEN:
                  classes_scores = row[5:]
                  if (classes_scores[np.argmax(classes_scores)] > SCORE_THRESHOLD_SCREEN):
                        cx, cy, w, h = row[0], row[1], row[2], row[3]
                        left = int((cx - w/2) * x_factor) 
                        top = int((cy - h/2) * y_factor) - 100
                        width = int(w * x_factor) 
                        height = int(h * y_factor) + 100
                        return crop(input_image, left, top, width, height)
      
      raise RuntimeError("No screen finded !")

def post_process_image_to_text(input_image, outputs, in_width, in_hieght):
      classes = DIGITS_LIST
      # Lists to hold respective values while unwrapping
      class_ids = []
      confidences = []
      boxes = []
      rows = outputs[0].shape[1]
      image_height, image_width = input_image.shape[:2]
      x_factor = image_width / INPUT_WIDTH
      y_factor =  image_height / INPUT_HEIGHT
      for r in range(rows):
            row = outputs[0][0][r]
            confidence = row[4]
            if confidence >= CONFIDENCE_THRESHOLD_DIGITS:
                  classes_scores = row[5:]                  
                  class_id = np.argmax(classes_scores)
                  if (classes_scores[class_id] > SCORE_THRESHOLD_DIGITS):
                        cx, cy, w, h = row[0], row[1], row[2], row[3]
                        left = int((cx - w/2) * x_factor)
                        top = int((cy - h/2) * y_factor)
                        width = int(w * x_factor)
                        height = int(h * y_factor)
                        box = np.array([left, top, width, height])

                        confidences.append(confidence)
                        class_ids.append(class_id)
                        boxes.append(box)
      
      indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD_DIGITS, NMS_THRESHOLD_DIGITS)
      
      sort_order = lambda x: x[0]
      msg = []
      for i in indices:
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            msg.append((left, classes[class_ids[i]]))

      msg.sort(key=sort_order)
      response = ''.join(digit[1] for digit in msg)
      cv2.putText(input_image, response, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
      return input_image, response