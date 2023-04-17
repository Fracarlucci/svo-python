from fastapi import HTTPException
from fastapi.responses import JSONResponse
import requests
import json
import urllib
from urllib.parse import urlencode
import urllib.parse
from MQTT_communication import mqtt
import logging

mode= "MQTT"
url= "http://tools.lysis-iot.com/MqttPublish/publish.php"


class communication_options:
    def get_sensor(self, name, reg_id):
        message = {"NAME": name.upper(), "COMMAND": "GET"}
        send.check_mode(send(), message, reg_id)

    def scheduleSensor(self, name, reg_id, interval):
        message =  {"NAME": name.upper(), "COMMAND": "SCHEDULE", "INTERVAL": str(interval)}
        send.check_mode(send(), message, reg_id)

    def setActuator(self, name, reg_id, value):
        message = {"NAME": name.upper(), "COMMAND": "SET", "VALUE": str(value)}
        send.check_mode(send(), message, reg_id)

    def get_scan(self, name, reg_id):
        message = {"NAME": name.upper(), "COMMAND": "SCAN"}
        send.check_mode(send(), message, reg_id)


class send():
    def check_mode(self,message, topic):
        if mode == "MQTT":
            return MQTT.send_mqtt(MQTT(), message, topic)
        if mode == "HTTP":
            return HTTP.send_http_post(HTTP(), message, topic)
        else:
            logging.warning("Error VoToDevice, class send(), check_mode() method.")
            raise HTTPException(status_code=400, detail="Wrong mode.")


class MQTT():
    def send_mqtt(self, message, topic):
        mqtt.subscribe(topic)
        mqtt.publish(str(topic), str(message))
        resp = json.dumps({"Response": "OK"})
        return JSONResponse(content=resp, status_code=200)

class HTTP():
    def send_http_post(self, message, topic):
        call = urllib.parse.urlencode({"topic": topic, "message": message})
        call = url + "?" + call
        response = requests.post(call)
