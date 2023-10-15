import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from northbound_api.handlers.base_trigger import BaseTrigger
from northbound_api.functions import Functions
from vo.models.Trigger import Trigger
from vo.models.Configuration import Configuration
from config import session, Base
import logging


class SetTrigger():

    body = None

    def __init__(self, request : Request):
        self.body = request.json()
        
    ##CHECK INPUTS
    ##QUERY SENSOR_NAME CORRISPONDENTE IN TABELLA CONFIGURATION
    def get_inputs(self):
        mandatory = ["event",
                    "feature",
                    "condition",
                    "value",
                    "output_method",
                    "output_value",
                    "output_address",
                    "app_id",
                    "key",
                    "status"]
        try:
            Functions.check_mandatory_parameters(Functions(), mandatory, self.body)
            BaseTrigger.get_configuration(BaseTrigger())
            return Configuration.query.get(self.body["feature"])
        except Exception:
            logging.warning("SetTrigger, get_inputs() method. Problem in check parameters or in get configuration")
            raise HTTPException(status_code=403, detail="Problem in check parameters or in get configuration")

    ##CHECK PERMESSI ( permission è un attributo presente nella tabella Configuration)
    #AGGIUNTA VALORI IN TABELLA TRIGGER
    def granted_actions(self):
        return_query= self.get_inputs()
        try:
            Functions.permissions(Functions(), self.body, return_query)
        except Exception:
            logging.warning("SetTrigger, granted_actions method. Problem in check permission")
            raise HTTPException(status_code=403, detail="Error in check permission")


        if self.body["status"] == "":
            status = "ON"
        else:
            status = self.body["status"]
        Base.metadata.create_all(tables=[Trigger])
        trigger = Trigger(event=self.body["event"], feature = self.body["feature"], value = self.body["value"],
                          output_method = self.body["output_method"], output_value = self.body["output_value"],
                          appID = self.body["app_id"], status = status, output_address = self.body["output_address"])
        session.add(trigger)
        session.commit()

        resp = json.dumps({"trigger_id": trigger.triggerID})
        return JSONResponse(content=resp, status_code=200)