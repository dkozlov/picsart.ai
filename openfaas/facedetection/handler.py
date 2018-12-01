import sys
import os
import io
import time
from flask import jsonify, send_file

import io
import base64
import json

from PIL import Image
import numpy as np
from mtcnn.mtcnn import MTCNN
detector = MTCNN()

def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    response = {'success': True}

    try:
        image = np.array(Image.open(io.BytesIO(req)))
        response['data'] = detector.detect_faces(image)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        #image_np = load_image_into_numpy_array(image)
        #pil_image = run_inference_for_single_image(image_np)
    except Exception as e:
        response['success'] = False
        response['message'] = str(e)
    #return serve_pil_image(pil_image)
    return json.dumps(response)
