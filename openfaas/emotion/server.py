from flask import Flask
from flask import request

import cv2
import numpy as np
import tensorflow as tf
from src.process import run

graph = None


app = Flask(__name__)

@app.route('/emotion', methods=['POST'])
def emotion():
    image = request.files['image']
    image_bytes = image.read()
    image_bytes_numpy = np.fromstring(image_bytes, np.uint8)
    
    img_numpy = cv2.imdecode(image_bytes_numpy, cv2.IMREAD_COLOR)
    img_size = img_numpy.shape
    
    emotions = run(graph, img_numpy)
    
    return "{}\n".format(emotions)

if __name__ == '__main__':
    graph = tf.get_default_graph()
    app.run()
