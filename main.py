from flask import Flask, render_template, request, Response
from camera import VideoCamera
import yaml
app = Flask(__name__)

videolive = 'rtsp://admin:admin@192.168.1.10:8554/live'


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        global videolive
        videolive = request.form['videolive']
        detection = request.form['detect']
        loglevel = request.form['log']
        streaming = request.form['stream']
        recording = request.form['record']
        jeedomalerting = request.form['alert']
        retention = request.form['retentionperiod']
        dict_file = [{'CAMERA': [videolive]}, {'DETECTION': [detection, loglevel, streaming, recording
                    , jeedomalerting]}, {'PURGE': [retention]}]
        with open("srv/config/configl.yaml", 'w') as file:
            documents = yaml.dump(dict_file, file)
        return render_template('/home.html', vlive=videolive, detect=detection, log=loglevel, stream=streaming,
                               record=recording, jalert=jeedomalerting, retperiod=retention)
    else:
        return render_template('/home.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

