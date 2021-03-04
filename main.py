import os
import datetime
from flask import Flask, render_template, request, Response
from camera import VideoCamera
import yaml
app = Flask(__name__)

# Ouverture du fichier config.dyn et récupération des valeurs
with open('static/srv/config/config.dyn') as f:
    data = yaml.safe_load(f)

vl = data[0]['CAMERA'][0]
dt = data[1]['DETECTION'][0]
ll = data[1]['DETECTION'][1]
sm = data[1]['DETECTION'][2]
rd = data[1]['DETECTION'][3]
ja = data[1]['DETECTION'][4]
rp = data[2]['PURGE'][0]


# Fonction qui convertit un string en date
def convert(dt):
    datei = datetime.datetime.strptime(dt[0:14], '%Y%m%d-%H%M%S')
    return datei


# Fonction qui permet le tri des dates
def tridate(a, b):
    if a.date() < b.date():
        return 1
    elif a.date() == b.date():
        if a.time() < b.time():
            return 1
        else:
            return 0
    else:
        return 0


# Définition de la route vers home
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    images_names = os.listdir('static/srv/img')  # Lecture de toutes les images du répertoire
    images_list = []
    for img in images_names:  # Initialisation du tri des dates en récupérant que les images .jpg
        if img[-3:] == "jpg":
            images_list.append(img)
    for y in range(len(images_list)):
        for i in range(1, len(images_list)):
            if tridate(convert(images_list[i - 1]), convert(images_list[i])) == 1:
                temp = images_list[i - 1]
                images_list[i - 1] = images_list[i]
                images_list[i] = temp

    if request.method == 'POST':  # Récupération du POST de la page home
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
            documents = yaml.dump(dict_file, file)  # Création du fichier config.dyn avec les valeurs du POST
        with open("static/srv/config/chgconfig", 'w') as file:
            document = yaml.dump("1", file)  # Création du fichier chgconfig
        return render_template('/home.html', vlive=videolive, detect=detection, log=loglevel, stream=streaming,
                               record=recording, jalert=jeedomalerting, retperiod=retention, images_list=images_list)
    else:
        return render_template('/home.html', vlive=vl, detect=dt, log=ll, stream=sm, record=rd, jalert=ja, retperiod=rp,
                               images_list=images_list)


def gen(camera):  # Initialisation de la caméra
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # Envoi du flux sur la page home
def video_feed():
    return Response(gen(VideoCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

