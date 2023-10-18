import logging
from config import session
from fastapi import HTTPException
from vo.models.VoInfo import VoInfo
from vo.models.Configuration import Configuration
from vo.models.Device_Id import Device_Id
from northbound_api.functions import Functions
import requests
from datetime import datetime
from southbound_api.vo_to_device.vo_to_device import communication_options
from vo.models.VoInfo import VoInfo


class commandController():
    this_svo = session.query(VoInfo).first()
    if this_svo is not None:
        #port = this_svo.vu_url.split(":")[2]
        url_to_send = "http://vu:" +str("1")+ "listener"
    def command_controller(self, command):
        if command["command"] == "SCHEDULE":

            try:
                mandatory = ["feature",
                             "schedule_interval"]
                Functions.check_mandatory_parameters(Functions(), mandatory, command)
            except Exception:

                requests.post(str(self.url_to_send), json = {"request_id": command["request_id"],
                                                                              "status_code": str("403"),
                                                                              "detail": "Missing parameters."})
                logging.warning("Missing parameters.")
                raise HTTPException(status_code=403, detail="Missing parameters.")
            sensor = Configuration.query.get(command["feature"])
            if sensor is not None:
                my_url = self.this_svo.url
                url_to_send = my_url + "set/schedule"
                payload = {"feature": command["feature"], "schedule_interval": command["schedule_interval"],
                           "key": self.this_svo.owner_key}
                resp = requests.post(url_to_send, data=payload)
                requests.post(str(self.url_to_send), json = {"request_id": command["request_id"],
                                                                              "status_code": str(resp.status_code),
                                                                              "detail": str(resp)})
            else:
                requests.post(str(self.url_to_send), json = {"request_id": command["request_id"],
                                                                              "status_code": "500",
                                                                              "detail": "No sensor for this feature."})

        if command["command"] == "GET":
            try:
                mandatory = ["feature",
                             "time_scope"]
                Functions.check_mandatory_parameters(Functions(), mandatory, command)
            except Exception:
                requests.post(str(self.url_to_send), json ={"request_id": command["request_id"],
                                                                              "status_code": str("403"),
                                                                              "detail": "Missing parameters."})
            sensor = Configuration.query.get(command["feature"])
            if sensor is not None:
                my_url = self.this_svo.url
                url_to_send = my_url + "get/sensor"
                payload = {"feature": command["feature"], "time_scope": command["time_scope"],
                          "key": self.this_svo.owner_key}
                resp = requests.post(url_to_send, data=payload)
                requests.post(str(self.url_to_send), json = {"request_id": command["request_id"],
                                                                              "status_code": str(resp.status_code),
                                                                              "detail": str(resp)})
            else:
                requests.post(str(self.url_to_send), json = {"request_id": command["request_id"],
                                                                              "status_code": "500",
                                                                              "detail": "No sensor for this feature."})
        if command["command"] == "GETNOW":
            dev = Device_Id.query.first()
            now = datetime.now()
            now_dt = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
            communication_options.get_sensor(communication_options(), command["feature"], str(dev.hal_key))
            requests.post(str(self.url_to_send), json= {"request_id": command["request_id"],
                                                                              "status_code": "200",
                                                                              "detail": now_dt})
            #successivamente vu puà fare richiesta del dato voluto tramite GET
