import json
from fastapi import Request
from fastapi.responses import JSONResponse
from northbound_api.functions import Functions
from vo.models.Configuration import Configuration
from vo.models.Trigger import Trigger

class StatusTrigger():

    trigger = None

    def __init__(self, trigger : dict):
        self.trigger = trigger

    ##CHECK INPUTS
    ##QUERY TRIGGER RICHIESTO
    def get_inputs(self):
        if self.trigger["trigger_id"] == "":
            mandatory= ["event",
                        "feature",
                        "condition",
                        "value",
                        "output_method",
                        "output_value",
                        "output_address",
                        "app_id",
                        "status"]
            Functions().check_mandatory_parameters(Functions(), mandatory, self.trigger)
            t = Trigger.query.filter_by(event=self.trigger["event"],
                                        condition=self.trigger["condition"],
                                        feature=self.trigger["feature"],
                                        appID=self.trigger["app_id"],
                                        output_method=self.trigger["output_method"],
                                        output_value=self.trigger["output_value"],
                                        output_address=self.trigger["output_address"]).first()
            trigger_id= t.triggerID
            return trigger_id
        else:
            return self.trigger["trigger_id"]

    def granted_actions(self):
        #CHECK PERMESSI
        ##CHECK STATUS TRIGGER
        trigger_id = self.get_inputs()
        t = Trigger.query.get(trigger_id)
        if t is None:
            return "No trigger for this id"
        return_query= Configuration.query.get(t.feature)
        code = Functions.permissions(Functions(), self.trigger, return_query)
        tr_status= t.status
        resp = json.dumps({"trigger_id":trigger_id,"status": tr_status})
        return JSONResponse(content=resp, status_code=200)


