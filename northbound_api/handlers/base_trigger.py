import json
from fastapi import HTTPException, Request
from vo.models.Configuration import Configuration
from vo.models.VoInfo import VoInfo
import logging

#I TRIGGER POSSONO ESSERE AGGIUNTI MA L'UNICO CHE VIENE EFFETTIVAMENTE CONTROLLATO è QUELLO SU ON BODY DEL VU
# PRATICAMENTE QUESTA PARTE TUTTA DA RIVEDERE E IMPLEMENTARE I CHECK SUI TRIGGER
class BaseTrigger():

    body = None

    def __init__(self, request : Request):
        self.body = request.json()

    def get_configuration(self):
        vo_info = VoInfo.query.first()
        if vo_info.owner_key != self.body["key"]:
            logging.warning("Wrong Key.")
            raise HTTPException(status_code=401, detail="Wrong Key.")
        conf_type = []
        if self.body["event"] == "SENSOR":
            return_query= Configuration.query.get(self.body["feature"])
            conf_type= return_query.type.split(",")

        sensor_condition_space = ["VERIFIED",
                                  "EQUAL",
                                  "NOT_EQUAL"]
        condition_space= sensor_condition_space
        print(conf_type)
        if "number" in conf_type:
            condition_space = condition_space + ["GREATER_THAN",
                                                        "GREATER_THAN_OR_EQUAL",
                                                        "LESS_THAN",
                                                        "LESS_THAN_OR_EQUAL"]
        if "position" in conf_type:
            condition_space = condition_space + ["IN_RANGE",
                                                       "OUT_RANGE",
                                                       "INPUT_RANGE",
                                                       "OUTPUT_RANGE"]
        if "text" in conf_type:
            condition_space = condition_space+ ["TECHNOLOGY_CHANGED",
                                                       "RSSI_CHANGED",
                                                       "STATUS_CHANGED"
                                                       ]
        if "number" not in conf_type and "position" not in conf_type and "text" not in conf_type:
                logging.warning("BaseTriggerHandler, get_configuration() method, no trigger for this type.")
                raise HTTPException(status_code=400, detail="No trigger for this type.")
        self.verify_condition_space(condition_space)
        self.validate_inputs(conf_type,type(self.body["value"]))


    def validate_inputs(self, conf_type, type):
        try:
            #if conf_type == "number":
            if "number" in conf_type and type in ["int", "float"]:
                self.check_number()

            #if "position" in conf_type:
                #self.check_position()

            if "text" in conf_type and type == 'str':
                self.check_text()

        except Exception:
            logging.warning("BaseTriggerHandler, validate_inputs() method. Error! Not done.")
            raise HTTPException(status_code=400, detail="Error! Not done.")
            #return "BaseTrigger, validate() method. Not done."

    def check_text(self):
        if self.body["condition"] == "TECHNOLOGY_CHANGED":
            value_space = ["WIFI", "LTE", "UMTS", "EDGE"]
            if self.body["value"].upper() not in value_space:
                logging.warning("BaseTriggerHandler, check_text() method, bad value.")
                raise HTTPException(status_code=400, detail="Bad value.")
        if self.body["condition"] == "STATUS_CHANGED":
            value_space = ["ONBODY"]
            if self.body["value"].upper() not in value_space:
                logging.warning("BaseTriggerHandler, check_text() method, bad value.")
                raise HTTPException(status_code=400, detail="Bad value.")
        elif self.body["condition"] == "RSSI_CHANGED":
            raise HTTPException(status_code=400, detail="Sorry, this condition type is not implemented yet.")


    def check_position(self):
        v = self.body["value"]
        if "shape" not in v and "params" not in v:
            logging.warning("BaseTriggerHandler, check_position() method")
            raise HTTPException(status_code=400, detail="Bad request. Please set value such as {'shape': 'your_shape', 'params': [...]}. Check documentation for more info")
        params = self.body["params"]
        if v["shape"].upper() == "CIRCLE":
            if "center" not in params and "radius" not in params:
                logging.warning("BaseTriggerHandler, check_position() method, missing circumference parameter")
                raise HTTPException(status_code=400, detail="Bad request. Please check center and radius keys")
            else:
                self.body["value"] = str(params["center"][0]) + "," + str(params["center"][0]) + ";" + str(params["radius"])
        elif v["shape"].upper() == "POLYLINE":
            pts = ""
            if len(params) <= 2:
                logging.warning("BaseTriggerHandler, check_position() method, not enough points in polyline")
                raise HTTPException(status_code=400, detail="Bad request. Please insert at least two points")
            for point in params:

                if len(point) != 2:
                    logging.warning("BaseTriggerHandler, check_position() method, bad point format")
                    raise HTTPException(status_code=400, detail="Bad request. Each point needs exactly two values")
                else:
                    pts += ";" + str(point[0]) + "," + str(point[1])
            self.body["value"] = pts

    def check_number(self):
        try:
            float(self.body["value"])
            print(self.body["value"])

        except Exception:
            logging.warning("BaseTriggerHandler, check_number() method")
            raise HTTPException(status_code=400, detail="Bad value format")



    def verify_condition_space(self, condition_space):
        condition = self.body["condition"]
        if condition not in condition_space:
            logging.warning("BaseTriggerHandler, check_condition_space() method")
            raise HTTPException(status_code=400, detail="Bad Request. Condition is not in condition_space for this feature.")







