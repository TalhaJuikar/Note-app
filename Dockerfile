FROM ubuntu

RUN apt update
RUN apt install -y python pyhton-pip

COPY ./requirements.txt /opt
COPY ./templates /opt/templates
COPY ./app.py /opt

RUN pip install -r /opt/requirements.txt

ENTRYPOINT python /opt/app.py

