from fastapi import HTTPException, Request
from vo.models.Device_Id import Device_Id
from vo.models.Data import Data
from vo.models.VoInfo import VoInfo
import config
import logging
from config import session
from datetime import datetime
from northbound_api.functions import Functions
# from MQTT_communication import mqtt
#from vu_interface.ControlHandlers.checkControl import checkControl_sensors
import requests

class SendData:   

    body = None

    def __init__(self, request : Request):
        self.body = request.json()

    def data_input(self):
        try:
            if self.body["feature"] == "" or self.body["type"] == "" or self.body["hal_key"] == "":
                logging.warning("SendDataHandler, data_input() method. Missing data")
                raise HTTPException(status_code=400, detail="Missing data")
            hal_key = self.body["hal_key"]
        except:
            return "Method not allowed"

        if config.cache.get(hal_key) is None:
            if  session.query(Device_Id).first() is None:
                logging.warning("SendDataHandler, data_input() method. It need to register device or wrong parameter 'hal_key'.")
                raise HTTPException(status_code=400, detail="Bad Request. It need to register device or wrong parameter 'hal_key'.")
            else:
                config.cache.set('hal_key', hal_key)
                self.data_db()
        return "Operation completed"



    def data_db(self):
        data = Data(feature = self.body["feature"], type = self.body["type"])
        ##se il dato è di tipo position, memorizza su database latitudine e longitudine formattate in json
        ##da rivedere trigger per dati del tipo position
        if self.body["type"]=="position":
            data += Data(value = str({"latitude":self.body["latitude"],"logitude":self.body["longitude"]}))
        else:
            data += Data(value = str(self.body["value"]))
        now = datetime.now()
        data += Data(timestamp = now) 
        config.cache.set('last_data_timestamp', str(now))
        session.add(data)
        session.commit()
        svo = VoInfo.query.first()
        url = svo.vu_url + "SendData"
        r = requests.post(url, json =self.body)
        print(r.text)
        #checkControl_sensors.check_control(checkControl_sensors(), dict(body))
        return "Data saved successful!"

    def validate(self):
        if self.body["type"] not in ["position", "mac-address", "number", "digital", "text"]:
            logging.warning("SendDataHandler, validate() method. Wrong parameter: {}.".format("type"))
            raise HTTPException(status_code=400, detail="Bad Request, wrong parameter '{}'.".format("type"))

        if self.body["type"] != "position" and ("latitude" in self.body.keys() or "longitude" in self.body.keys()):
            logging.warning("SendDataHandler, validate() method. Wrong parameters latitude and longitude.")
            raise HTTPException(status_code=400, detail="Bad Request, wrong parameters 'latitude or longitude' with type '{}'.".format(self.body["type"]))

        if self.body["type"] == "position" and ("value" in self.body.keys() or "latitude" not in self.body.keys() or "longitude" not in self.body.keys()):
            logging.warning("SendDataHandler, validate() method. Wrong parameter value or missing latitude/longitude value.")
            raise HTTPException(status_code=400, detail="Bad Request, wrong parameter 'value' with type '{}'.".format(self.body["type"]))

        #se vongono ricevute latitudine e longitudine, check locaion_id e pubblica messaggio sulla subscribe corrispondente
        if self.body["type"] == "position" and ("latitude" in self.body.keys() and "longitude" in self.body.keys()):
            if session.query(VoInfo).first() is not None:
                item = session.query(VoInfo).first()
                timestamp = config.cache.get('last_data_timestamp')
                tm = config.cache.delete("last_data_timestamp")
                print(tm)
                msg = {"svo_url": item.url, "type":"mobile", "timestamp":timestamp}
                location=Functions.search_place(Functions(), float(self.body["latitude"]), float(self.body["longitude"]))
                print(location)
                id = location["location_id"]
                # mqtt.subscribe(str(id))
                Functions.send_message_mqtt(Functions(), str(id), str(msg))

        ##se viene ricevuto mac-address da sensore, pubblica un messaggio sulla subscribe equivalente
        #if body["type"]=="mac-address":
          #  if session.query(VoInfo).first() is not None:
           #     item=VoInfo.query.first()
           #     if item.location == "fixed":
           #         msg = {"svo_url": item.url, "type": "fixed"}
           #     else:
           #         msg = {"svo_url": item.url}
            #    mqtt.subscribe((str(body["value"])))
            #    Functions.send_message_mqtt(Functions(), str(body["value"]), str(msg))

        return "Validation completed"
