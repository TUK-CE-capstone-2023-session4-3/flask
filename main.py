from flask import Flask, render_template, Response
from camera import VideoCamera
from IPython.display import display, Javascript, Image
from google.colab.output import eval_js
from google.colab.patches import cv2_imshow
from base64 import b64decode, b64encode
import cv2
import numpy as np
from flask_ngrok import run_with_ngrok
# import PIL
import io
import html
import time

# import matplotlib.pyplot as plt
# %matplotlib inline


app = Flask(__name__)
run_with_ngrok(app)


def video_frame(label, bbox):
  data = eval_js('stream_frame("{}", "{}")'.format(label, bbox))
  return data

def gen(camera):
    while True:
        # frame = camera.get_frame()
        frame_js = video_frame()
        frame = camera.jsob_to_image(frame_js["img"])
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
@app.route('/')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
    app.run()



# JavaScript to properly create our live video stream using our webcam as input
