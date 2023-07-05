import cv2

# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 480

SCORE_THRESHOLD_SCREEN = 0.5
NMS_THRESHOLD_SCREEN = 0.3
CONFIDENCE_THRESHOLD_SCREEN = 0.3

SCORE_THRESHOLD_DIGITS = 0.6
NMS_THRESHOLD_DIGITS = 0.5
CONFIDENCE_THRESHOLD_DIGITS = 0.4

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1
 
# Colors.
BLACK  = (0,0,0)
BLUE   = (255,178,50)
YELLOW = (0,255,255)
DIGITS_LIST = (
                "0", "1", "2",
                "3", "4", "5",
                "6", "7", "8",
                "9", "-", ".",
                "L"
            )

# Weights
SCREEN_WEIGHTS = r"wieghts\display.onnx" 
DIGITS_WEIGHTS = r"wieghts\model.onnx"

SCREEN_NET = cv2.dnn.readNetFromONNX(SCREEN_WEIGHTS)
DIGITS_NET = cv2.dnn.readNetFromONNX(DIGITS_WEIGHTS)
