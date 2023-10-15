import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from northbound_api.functions import Functions
from northbound_api.handlers.base_trigger import BaseTrigger
from vo.models.Control import Control
from config import session
import logging

class setControl():
    ##CHECK INPUTS and OWNER KEY
    def set_control(self, request: Request):
        body = request.json()
        mandatory = ["condition",
                     "event",
                     "feature",
                     "value",
                     "key"]
        try:
            Functions.check_mandatory_parameters(Functions(), mandatory, body)
            BaseTrigger.get_configuration(BaseTrigger())
        except Exception:
            logging.warning("SetControl, set_control() method. Problem in check parameters or get_configuration.")
            raise HTTPException(status_code=403, detail="Problem in set_control() - 1.")
        try:
            return self.add_control(dict(body))
        except Exception:
            logging.warning("SetControl, set_control() method. Problem in adding control to database.")
            raise HTTPException(status_code=403, detail="Problem in set_control() - 2")


    #AGGIUNTA VALORI IN TABELLA CONTROL
    def add_control(self, body):
        session.create_all()
        control = Control()
        control.condition = body["condition"]
        control.event = body["event"]
        control.feature = body["feature"]
        control.value = body["value"]
        control.status = "ON"
        session.add(control)
        session.commit()
        resp = json.dumps({"control_id": control.controlID})
        return JSONResponse(content=resp, status_code=200)