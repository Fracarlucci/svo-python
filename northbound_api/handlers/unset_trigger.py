import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from northbound_api.functions import Functions
from vo.models.Configuration import Configuration
from vo.models.Trigger import Trigger
import logging
from config import session


class UnsetTrigger:

    trigger = None

    def __init__(self, trigger : dict):
        self.trigger = trigger

    ##CHECK INPUTS
    ##QUERY SENSOR_NAME CORRISPONDENTE IN TABELLA CONFIGURATION
    def get_inputs(self):
        mandatory = ["event",
                     "trigger_id",
                     "condition",
                     "value",
                     "output_method",
                     "output_value",
                     "scope",
                     "key",
                     "feature"]

        try:
            Functions.check_mandatory_parameters(Functions(), mandatory, self.trigger)
            return Configuration.query.get(self.trigger["feature"])
        except Exception:
            logging.warning("UnsetTrigger, get_inputs method. Error !!")
            raise HTTPException(status_code=400, detail="Error in get_inputs")



    def granted_actions(self):
        ##CHECK PERMESSI ( SOLO FRIEND E OWNER)
        ##QUERY SU TRIGGER IN BASE AD ATTRIBUTO "scope"
        return_query= self.get_inputs()
        code = Functions.permissions(Functions(), self.trigger, return_query)
        scope = self.trigger["scope"]
        if code == 0:
            logging.warning("UnsetTrigger, granted_actions.")
            raise HTTPException(status_code=400, detail="Permission not granted")
        if scope == "ONE":
            if self.trigger["trigger_id"] == "":
                if Trigger.query.filter_by(event=self.trigger["event"], feature=self.trigger["feature"], output_method=self.trigger["output_method"],
                                           output_value=self.trigger["output_value"]).first() is not None:
                    d=Trigger.query.filter_by(
                                            event=self.trigger["event"],
                                            feature=self.trigger["feature"],
                                            output_method=self.trigger["output_method"],
                                            output_value=self.trigger["output_value"]).delete()

                    session.commit()
                    resp = json.dumps({"deletion Trigger/Triggers": "Successful"})
                    return JSONResponse(content=resp, status_code=200)

                else:
                        logging.warning("UnsetTrigger, granted_actions() method. Trigger not found.")
                        raise HTTPException(status_code=410, detail="The trigger with that parameters does not exists")
            else:
                    d= Trigger.query.filter_by(triggerID=self.trigger["trigger_id"]).first()
                    if d is not None:
                        session.delete(d)
                        session.commit()
                        resp = json.dumps({"deletion Trigger": "Successful"})
                        return JSONResponse(content=resp, status_code=200)

                    else:
                        logging.warning("UnsetTrigger, granted_actions() method. Trigger not found.")
                        raise HTTPException(status_code=410, detail="This trigger does not exists")

        if scope=="ALL":
            feature=self.trigger["feature"]
            if feature is not None:
                if Trigger.query.filter_by(feature=self.trigger["feature"]).first() is not None:
                    Trigger.query.filter_by(feature=self.trigger["feature"]).delete()
                    session.commit()
                    resp = json.dumps({"Deletion ALL triggers": "Successful"})
                    return JSONResponse(content=resp, status_code=200)
                else:
                    logging.warning("UnsetTrigger, granted_actions() method. Trigger not found.")
                    raise HTTPException(status_code=410, detail="No triggers found.")
            else:
                logging.warning("UnsetTrigger, granted_actions() method. Trigger not found.")
                raise HTTPException(status_code=410, detail="Feature is None")
