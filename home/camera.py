# import facerecoginition
import cv2
from urllib3 import request
import numpy as np

class VideoCapture(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, img = self.video.read()
        return cv2.imencode('.jpg', cv2.flip(img, 1))[-1].tobytes()