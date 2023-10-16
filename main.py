from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_cors import CORS
camera_instance = VideoCamera()
app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('index.js')
    
def gen(camera):
    global label
    label = None
    while True:
        frame, label = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               
@app.route('/video_feed')
def video_feed():
    return Response(gen(camera_instance),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_label')
def video_label():
    if camera_instance.fall_detected == 1:
        return Response('1')
    else:
        return Response('0')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
