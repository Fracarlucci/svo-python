import json
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config import session
from vo.models.Configuration import Configuration
from northbound_api.functions import Functions
from sqlalchemy import or_
import logging


class Feature:

    def get_feature_list(self, key):
        #ACQUISIZIONE PARAMETRO URLENCODE
        user_data = {}
        user_data['key'] = key
        ##la chiave non viene fornita ->  feature con permessi public
        ##chiave friend -> feature con permessi public e friend
        ##chiave owner -> tutte le feature

        if user_data['key'] == "":
            data_list = session.query(Configuration).filter_by(permission="public").all()
            response = [{"feature": (d.feature), "name": (d.name)} for d in data_list]
            resp=json.dumps({"The feature list is": response})
            return JSONResponse(content=resp, status_code=200)
        else:
            level= Functions.get_permission_level(Functions(), user_data['key'])
            if level == "friend":
                data_list = session.query(Configuration).filter_by(permission="friend").all()
                filter_rule = or_(Configuration.permission=="friend", Configuration.permission=="public")
                data_list = session.query(Configuration).filter(filter_rule).all()
                response = [{"feature": (d.feature), "name": (d.name)} for d in data_list]
                resp = json.dumps({"The feature list is": response})
                return JSONResponse(content=resp, status_code=200)
            if level == "owner":
                data_list = session.query(Configuration).all()
                response = [{"feature": (d.feature), "name": (d.name)} for d in data_list]
                resp = json.dumps({"The feature list is": response})
                return JSONResponse(content=resp, status_code=200)
            else:
                logging.warning("GetFeatureList, getList_feature() method. Wrong key")
                raise HTTPException(status_code=400, detail="Bad request. Please check key parameter")
