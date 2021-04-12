# import facerecoginition
# import numpy as np
import cv2, os
from django.conf import settings 

# for temprary purpose remove face_detection_data, settings import 
# when facerecoginition lib will be added

#################################################################################
face_detection_data = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR, 'static/data_set/haarcascade_frontalface_default.xml'))
#################################################################################

class VideoCapture(object):
    def __init__(self, id):
        self.video = cv2.VideoCapture(id)
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, img = self.video.read()
        # open-cv code for face detection replace it with facerecoginition code
        ###############################################################################
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detection_data.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x,y,w,h) in faces_detected: cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h), color=(0, 0, 255), thickness=2)
        ###############################################################################
        return cv2.imencode('.jpg', cv2.flip(img, 1))[-1].tobytes()