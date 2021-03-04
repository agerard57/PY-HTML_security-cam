FROM arm32v7/python:3.9-slim-buster 

RUN apt-get clean apt-get update   

COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt

ADD . /srv/
WORKDIR /srv

EXPOSE 5250

CMD ["python","main.py"]
