import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from northbound_api.functions import Functions
from config import session
from vo.models.VoInfo import VoInfo
from vo.models.Control import Control
import logging

class statusControl():
    def check_status(request: Request):
        body= request.json()
        if "key" not in body.keys() :
            logging.warning("statusControl, check_status(). Missing key. ")
            raise HTTPException(status_code=403, detail="Missing key.")
        vo_info = VoInfo.query.first()
        if vo_info.owner_key != body["key"]:
            logging.warning("Wrong Key.")
            raise HTTPException(status_code=401, detail= "Wrong Key.")
        if body["control_id"] == "":
            mandatory= ["event",
                        "feature",
                        "condition",
                        "value",
                        ]
            Functions().check_mandatory_parameters(Functions(), mandatory)
            control = Control.query.filter_by(event=body["event"],
                                        condition=body["condition"],
                                        feature=body["feature"],
                                        value=body["value"]).first()
            id= control.ControlID
        else:
            id = body["control_id"]
        c = Control.query.get(id)
        if c is None:
            return "No control setted for this id."
        resp = json.dumps({"control_id":id,"status": c.status})
        return JSONResponse(content=resp, status_code=200)
    
    def change_status(request: Request):
        body = request.json()
        if "key" not in body.keys():
            logging.warning("statusControl, change_status(). Missing key. ")
            raise HTTPException(status_code=403, detail="Missing key.")
        vo_info = VoInfo.query.first()
        if vo_info.owner_key != body["key"]:
            logging.warning("Wrong Key.")
            raise HTTPException(status_code=401, detail= "Wrong Key.")
        if body["control_id"] == "":
            mandatory = ["event",
                         "feature",
                         "condition",
                         "value",
                         ]
            Functions().check_mandatory_parameters(Functions(), mandatory)
            control = Control.query.filter_by(event=body["event"],
                                              condition=body["condition"],
                                              feature=body["feature"],
                                              value=body["value"]).first()
            id = control.ControlID
        else:
            id = body["control_id"]
        c = Control.query.get(id)
        if c is None:
            return "No control setted for this id."
        if c.status == "ON":
            c.status = "OFF"
            session.add(c)
            session.commit()
        elif c.status == "OFF":
            c.status = "ON"
            session.add(c)
            session.commit()
        else:
            return "Invalid status for this control."
        resp = json.dumps({"control_id": id, "new_status": c.status})
        return JSONResponse(content=resp, status_code=200)