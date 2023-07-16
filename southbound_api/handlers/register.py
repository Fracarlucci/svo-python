from fastapi import HTTPException, Request
from db.Device_Id import Device_Id
from db.Configuration import Configuration
import logging
from vo.platform.registration.registration import registration
import config
from config import session, Base
from SVO.utils.send_message import SendMessage
from MQTT_communication import mqtt


class Register:

    body = None

    def __init__(self, request : Request):
        self.body = request.json()

    #Controlla che il device non sia già registrato ( sia in database che in cache)
    def check_device(self):
        if self.body["brand"] == "" or self.body["model"] == "" or self.body["hal_key"]== "" or self.body["configuration"] == "":
            logging.warning("RegisterHandler, missing data")
            raise HTTPException(status_code=400, detail="Bad request. Missing Data")
        if config.cache.get('hal_key') is True:
            logging.warning("Register, HalKey in memcache. Device already associated.")
            raise HTTPException(status_code=400, detail="Bad request. Device already associated (Cache)")
        else:
            if session.query(Device_Id).first() is not None:
                logging.warning("Register, device in datastore. Device already associated (DB).")
                raise HTTPException(status_code=400, detail="Bad request. Device already associated")
            else:
                self.add_device()

    def add_device(self):
        #registra device in db
        Base.metadata.create_all(tables=[Device_Id])
        device_id = Device_Id(hal_key = self.body["hal_key"])
        session.add(device_id)
        session.commit()
        #comunicazioni con vo
        mqtt.subscribe(self.body["hal_key"])

    def configuration(self):
        #registra configurazione device
        try:
            config_template = {"event": ["sensor", "actuator"],
                               "type": 0,
                               "feature": 0,
                               "permission": ["public", "private", "friend"],
                               "schedulable": ["True", "False"]}
            for element in self.body["configuration"]:
                for key in config_template.keys():
                    missing_parameter = key
                    _ = element[key]
                    if isinstance(config_template[key], list):
                        if element[key] not in config_template[key]:
                            logging.warning("Register, configuration, Wrong parameter:{}.".format(missing_parameter))
                            raise HTTPException(status_code=400, detail="Register, configuration, Bad Request, wrong parameter '{}'.".format(missing_parameter))
                if element["feature"] == "actuator" and element["schedulable"] is True:
                    logging.warning("Register, configuration, Wrong parameter: {}. It's can not be ""True with actuator feature".format("schedulable"))
                    raise HTTPException(status_code=400, detail="Register, configuration, Bad Request, wrong parameter '{}' in Actuator.".format("schedulable"))
        except Exception:
            logging.warning("Register, configuration, Missing configuration parameter: {}.".format(missing_parameter))
            raise HTTPException(status_code=400, detail="Register, configuration, Bad Request, missing parameter '{}'".format(missing_parameter))

        #possono essere registrari più sensori/attuatori per svo
        for i in self.body["configuration"]:
            print(i)
            configuration = Configuration(event = i["event"], type = i["type"], feature = i["feature"],
                                          permission = i["permission"], schedulable = i["schedulable"])
            session.add(configuration)
            session.commit()
        config.cache.set('hal_key', self.body["hal_key"])

    def update_vo_info(self):
        #aggiorna info device
        item = session.query.first()
        for key, value in self.body:
            setattr(item, key, value)

        ##se vengono fornite lat e lng, tramite google places viene calcolato location_id
        #il VO trasmette tramite MQTT
        if self.body["latitude"] !="" and self.body["longitude"] !="":
            location = SendMessage.google_id(SendMessage(), float(self.body["latitude"]), float(self.body["longitude"]))
            setattr(item, "location_name", location["location_name"]) 
            setattr(item, "location_range", location["location_range"]) 

            #location fornita in fase di registrazione : fixed o mobile
            msg = {"svo_url": item.url, "type": self.body["location"], "tag":location["location_name"]}
            SendMessage.send(SendMessage(), location["location_id"], msg)
        session.add(item)
        session.commit()
        session.refresh(item)
        return "update VoInfo success!!"

    def platform(self):
        #registra il device in piattaforma
        #NON SERVE CON VU
        r_code = registration(self.body["url"], self.body["brand"], self.body["model"], self.body["w_mac"], self.body["b_mac"])

        if r_code == 200:
            return "Registration success!!"
        else:
            logging.warning("Register, error in registration in platform.")
            raise HTTPException(status_code=400, detail="Bad request. Error in registration!")
