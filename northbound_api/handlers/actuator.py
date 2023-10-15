import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from northbound_api.functions import Functions
from vo.models.Configuration import Configuration
from vo.models.Device_Id import Device_Id
import logging
from southbound_api.vo_to_device.vo_to_device import communication_options

class SetActuator():
    body = None

    def __init__(self, request : Request):
        self.body = request.json()

    ##CHECK INPUTS
    ## QUERY SENSOR_NAME CORRISPONDENTE IN TABELLA CONFIGURATION
    ##CHECK FEATURE PARAMETER
    def get_inputs(self):
        mandatory = ["feature",
                     "value"]
        Functions.check_mandatory_parameters(Functions(), mandatory, self.body)
        return_query = Configuration.query.get(self.body["feature"])
        print (return_query.feature)
        try:
            event = return_query.event
            if event != "actuator":
                logging.warning("SetActuator, get_input() method. Not actuator.")
                raise HTTPException(status_code=400, detail="Bad request. The resource is not an actuator.")
            else:
                return return_query
        except Exception:
            logging.warning("SetActuator, get_input() method. Missing feature parameter.")
            raise HTTPException(status_code=400, detail="Bad request. Missing feature parameter.")

    def granted_actions(self):
        ##CHECK PERMESSI ( permission è un attributo presente nella tabella Configuration)
        ##INVIO COMANDO TRAMITE MQTT
        return_query = self.get_inputs()
        try:
            Functions.permissions(Functions(), self.body, return_query)
        except Exception:
            logging.warning("GetSchedule, granted_actions method. Not allowed.")
            raise HTTPException(status_code=403, detail="Not Allowed")
        actuator_feature = self.body["feature"]
        value = self.body["value"]
        #message=json.dumps({"actuator name" :actuator_name, "value:": value})
        #id = Config.cache.get('hal_key')
        ##passa json
        dev = Device_Id.query.first()
        communication_options.setActuator(communication_options(), actuator_feature, dev.hal_key, value)
        resp = json.dumps({"Actuator setted status": "OK"})
        return JSONResponse(content=resp, status_code=200)
