from flask import Flask, render_template, request, Response
from camera import VideoCamera
import yaml
app = Flask(__name__)

'''videolive = 'rtsp://admin:admin@192.168.1.10:8554/live'''

with open('static/srv/config/config.dyn') as f:
    data = yaml.safe_load(f)

vl = data[0]['CAMERA'][0]
dt = data[1]['DETECTION'][0]
ll = data[1]['DETECTION'][1]
sm = data[1]['DETECTION'][2]
rd = data[1]['DETECTION'][3]
ja = data[1]['DETECTION'][4]
rp = data[2]['PURGE'][0]

total = float(rp)*3600


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        videolive = request.form['videolive']
        detection = request.form['detect']
        loglevel = request.form['log']
        streaming = request.form['stream']
        recording = request.form['record']
        jeedomalerting = request.form['alert']
        retention = request.form['retentionperiod']
        dict_file = [{'CAMERA': [videolive]}, {'DETECTION': [detection, loglevel, streaming, recording
                    , jeedomalerting]}, {'PURGE': [retention]}]
        with open("static/srv/config/config.dyn", 'w') as file:
            documents = yaml.dump(dict_file, file)
        with open("static/srv/config/chgconfig", 'w') as file:
            document = yaml.dump("1", file)
        return render_template('/home.html', vlive=videolive, detect=detection, log=loglevel, stream=streaming,
                               record=recording, jalert=jeedomalerting, retperiod=retention)
    else:
        return render_template('/home.html', vlive=vl, detect=dt, log=ll, stream=sm, record=rd, jalert=ja, retperiod=rp)


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
    app.run(debug=True, host="127.0.0.1", port="5100")


