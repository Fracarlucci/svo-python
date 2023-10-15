import json
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from northbound_api.functions import Functions
from vo.models.VoInfo import VoInfo
from vo.models.Control import Control
import logging
from config import session


class unsetControl():
    def unset_control(request: Request):
        body = request.json()
        if "key" not in body.keys():
            logging.warning("statusControl, unset_status(). Missing key. ")
            raise HTTPException(status_code=403, detail="Missing key.")
        if "scope" not in body.keys():
            logging.warning("statusControl, unset_status(). Missing scope value. ")
            raise HTTPException(status_code=403, detail="Missing scopevalue.")
        vo_info = VoInfo.query.first()
        if vo_info.owner_key != body["key"]:
            logging.warning("Wrong Key.")
            raise HTTPException(status_code=401, detail="Wrong Key.")
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
        scope = body["scope"]
        if scope == "ONE":
            if body["control_id"] =="":
                if Control.query.filter_by(event=body["event"], feature=body["feature"], condition=body["condition"],
                                           value=body["value"]).first() is not None:
                    Control.query.filter_by( event=body["event"], feature=body["feature"], condition=body["condition"],
                                            value=body["value"]).delete()
                    session.commit()
                    resp = json.dumps({"deletion Control/Controls": "Successful"})
                    return JSONResponse(content=resp, status_code=200)
                
                else:
                        logging.warning("unsetControl, unset_control() method. Control not found.")
                        raise HTTPException(status_code=410, detail="The Control with that parameters does not exists.")
            else:
                    c = Control.query.filter_by(controlID=body["control_id"]).first()
                    if c is not None:
                        session.delete(c)
                        session.commit()
                        resp = json.dumps({"deletion Control": "Successful"})
                        return JSONResponse(content=resp, status_code=200)
                    else:
                        logging.warning("unsetControl, unset_control() method. Control not found.")
                        raise HTTPException(status_code=410, detail="This control does not exists.")

        if scope=="ALL":
            event=body["event"]
            if event is not None:
                if Control.query.filter_by(event=body["event"]).first() is not None:
                    Control.query.filter_by(event=body["event"]).delete()
                    session.commit()
                    resp = json.dumps({"Deletion ALL controls": "Successful"})
                    return JSONResponse(content=resp, status_code=200)                
                else:
                    logging.warning("unsetControl, unset_control() method. Control not found.")
                    raise HTTPException(status_code=410, detail="No controls found.")
            else:
                logging.warning("unsetControl, unset_control() method. Control not found.")
                raise HTTPException(status_code=410, detail="Event is None.")










