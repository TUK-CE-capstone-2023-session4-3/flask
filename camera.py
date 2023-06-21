import cv2


class VideoCamera(object):
    def __init__(self):
      self.video = cv2.VideoCapture(0)
    def __del__(self):
      self.video.release()
    def get_frame(self):
      ret, frame = self.video.read()
      # frame = cv2.flip(frame, 1) flip \
      print("\nasdsada\n",self)
      ret, jpeg = cv2.imencode('.jpg', frame)
      return jpeg.tobytes()
