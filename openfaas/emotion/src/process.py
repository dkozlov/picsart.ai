import sys
import os
import json

REL_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REL_PATH)

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input


# parameters for loading data and images
detection_model_path = 'trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path ='trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')

emotion_label_list = []
for k in sorted(emotion_labels.keys()):
    emotion_label_list.append(emotion_labels[k])
    
font = cv2.FONT_HERSHEY_SIMPLEX

# hyper-parameters for bounding boxes shape
emotion_offsets = (20, 40)
emotion_offsets = (0, 0)  # WTF


# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]


def run(graph, bgr_image):
    if True:
        image_path = 'temp.jpg'
        cv2.imwrite(image_path, bgr_image)
        rgb_image = load_image(image_path, grayscale=False)
        gray_image = load_image(image_path, grayscale=True)
        
    else:
        #todo: don't save to disk
        pass
    
        
    gray_image = np.squeeze(gray_image)
    gray_image = gray_image.astype('uint8')
    
    faces = detect_faces(face_detection, gray_image)
    face_emotions = []
    
    for face_coordinates in faces:
        face_dict = {}
        
        # face detection
        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue
        face_dict['bbox'] = [str(x1), str(x2), str(y1), str(y2)]
        
        # emotion detection
        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        with graph.as_default():
            emotion_probs = emotion_classifier.predict(gray_face)
            emotion_dict = {}
            for idx, name in enumerate(emotion_label_list):
                emotion_dict[name] = '{:.2f}'.format(emotion_probs[0][idx])
            emotion_label_arg = np.argmax(emotion_probs)
        face_dict['emotions'] = emotion_dict

        face_emotions.append(face_dict)
        
    return json.dumps(face_emotions)
