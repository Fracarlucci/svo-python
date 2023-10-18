FROM python:3.11
RUN mkdir /svo
WORKDIR /svo
COPY ./requirements.txt /svo/requirements.txt
RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip
RUN pip install -r /svo/requirements.txt
COPY . /svo/
CMD python ./app_mqtt.py
