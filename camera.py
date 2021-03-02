from datetime import datetime
import cv2
import yaml

with open('static/srv/config/config.dyn') as f:
    data = yaml.safe_load(f)


class VideoCamera(object):

    date = datetime.today().strftime('%Y%m%d-%H%M%S')
    filename = "srv/img/"+date + "-MicroSec.avi"
    frames = 10.0
    my_res = '480p'
    dims = {
        "480p": (640, 480),
    }

    '''out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), frames, dims['480p'])'''

    def __init__(self):
        self.video = cv2.VideoCapture(data[0]['CAMERA'][0])
        '''self.video = cv2.VideoCapture('rtsp://192.168.1.10:8080')'''

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        '''out.write(frame)'''
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
