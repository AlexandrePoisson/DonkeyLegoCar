import cv2
ds_factor=0.6

GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

class VideoCamera(object):
    def __init__(self):
       self.video = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
    def __del__(self):
       self.video.release()
    def get_frame(self):
       ret, frame = self.video.read()
       frame = cv2.resize(frame,None,fx=ds_factor,fy=ds_factor, interpolation = cv2.INTER_AREA)                    
       ret, jpeg = cv2.imencode('.jpg', frame)
       return jpeg.tobytes()
