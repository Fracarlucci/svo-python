from fastapi import HTTPException, Request
from vo.models.Device_Id import Device_Id
from vo.models.VoInfo import VoInfo
from vo.models.Configuration import Configuration
import logging
# from vo.platform.registration.registration import registration
from config import session, Base
from SVO.utils.send_message import SendMessage
import device_comm
import SVO.utils.svo_mqtt_comm as mqtt_comm

class Register:

    @classmethod
    async def create(self, request : Request):
        self = Register()
        self.body = await request.json()
        return self

    #Controlla che il device non sia già registrato ( sia in database che in cache)
    async def check_device(self):

        if (self.body["brand"] == "" or self.body["model"] == "" or self.body["hal_key"]== ""
                or self.body["location"] == "" or self.body["configuration"] == ""):
            logging.warning("RegisterHandler, missing data")
            raise HTTPException(status_code=400, detail="Bad request. Missing Data")
        else:
            if session.query(Device_Id).first() is not None:
                logging.warning("Register, device in datastore. Device already associated (DB).")
                raise HTTPException(status_code=400, detail="Bad request. Device already associated")
            else:
                await self.add_device()

    async def add_device(self):
        #registra device in db
        vo_info = session.query(VoInfo).first()
        device_id = Device_Id(hal_key = self.body["hal_key"])
        session.add(device_id)
        
        for key, value in self.body.items():
            setattr(vo_info, key, value)
        session.commit()

        # comunicazioni con device e CLOR relationship
        device_comm.set_up_mqtt(self.body["hal_key"])
        mqtt_comm.subscribe_to(self.body["location"] + "/discover", vo_info.url)

    async def configuration(self):
        #registra configurazione device
        try:
            config_template = {"event": ["sensor", "actuator"],
                               "type": "",
                               "feature": "",
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
        # config.cache.set('hal_key', self.body["hal_key"])

    # async def platform(self):
    #     #registra il device in piattaforma
    #     #NON SERVE CON VU
    #     r_code = registration(self.body["url"], self.body["brand"], self.body["model"], self.body["w_mac"], self.body["b_mac"])

    #     if r_code == 200:
    #         return "Registration success!!"
    #     else:
    #         logging.warning("Register, error in registration in platform.")
    #         raise HTTPException(status_code=400, detail="Bad request. Error in registration!")
