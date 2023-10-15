import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from vo.models.Configuration import Configuration
from northbound_api.functions import Functions
import logging

class GetSchedule():

    sensor_feature = None

    def __init__(self, feature : str):
        self.sensor_feature = feature

    ##CHECK INPUTS
    ##QUERY SENSOR_NAME CORRISPONDENTE IN TABELLA CONFIGURATION
    def get_inputs(self):
        mandatory = ["sensor_feature"]
        Functions.check_mandatory_parameters(Functions(), mandatory, self.sensor_feature)
        return_query = Configuration.query.get(self.sensor_feature)
        return return_query

    ##CHECK PERMESSI ( permission è un attributo presente nella tabella Configuration)
    ##STAMPA schedule_interval CORRISPONDENTE
    def granted_actions(self):
        return_query = self.get_inputs()
        try:
            Functions.permissions(Functions(), self.sensor_feature, return_query)
        except Exception:
            logging.warning("GetSchedule, granted_actions method. Problem in check permission")
            raise HTTPException(status_code=403, detail="Error in check permission")

        resp = json.dumps({"schedule_interval": return_query.schedule})
        return JSONResponse(content=resp, status_code=200)