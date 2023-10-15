import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from vo.models.Configuration import Configuration
from vo.models.Device_Id import Device_Id
from northbound_api.functions import Functions
from config import session
import logging
from southbound_api.vo_to_device.vo_to_device import communication_options


class SetSchedule():

    body = None

    def __init__(self, request : Request):
        self.body = request.json()

    ##CHECK INPUTS
    ##QUERY sensor_name CORRISPONDENTE IN TABELLA CONFIGURATION
    def get_inputs(self):
        mandatory = ["feature",
                     "schedule_interval"]
        Functions.check_mandatory_parameters(Functions(), mandatory, self.body)

        return_query = Configuration.query.get(self.body["feature"])
        return return_query

    ##CHECK PERMESSI
    ##CARICA NUOVO VALORE ATTRIBUTO schedule CORRISPONDENTE in database
    ##lo manda anche al sensore
    ##STAMPA CODICE PERMESSO E MESSAGGIO DI AVVENUTO AGGIORNAMENTO
    def granted_actions(self):
        return_query= self.get_inputs()
        try:
            permission_code= Functions.permissions(Functions(),self.body, return_query)
            resp = json.dumps({"code": permission_code, "message": "schedule_interval updated"})
            return_query.schedule = int(self.body["schedule_interval"])
            session.commit()
            dev = Device_Id.query.first()
            communication_options.scheduleSensor(communication_options(), return_query.feature, dev.hal_key, return_query.schedule)
            return JSONResponse(content=resp, status_code=200)
        except Exception:
            logging.warning("SetSchedule, granted_actions method. Not allowed.")
            raise HTTPException(status_code=403, detail="Not Allowed")


