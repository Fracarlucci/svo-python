import json, logging
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from vo.models.VoInfo import VoInfo
from vo.models_svo.ListsRelationship import ListsRelationship
from config import session

class InitializeRelationship():
    async def initialize_relationship(request : Request):
        ##Memorizza liste di inizializzazione in tabella ausiliaria RELATIONSHIP
        ##OOR e POR
        body = await request.json()
        vo_info = session.query(VoInfo).first()
        init_rel = session.query(ListsRelationship).first()
        if vo_info is None:
            logging.warning("InitializeRelationship, no values in VoInfo ")
            raise HTTPException(status_code=400, detail="VoInfo empty")

        if init_rel is None:
            if vo_info.owner == body["owner"] and vo_info.owner_key == body["owner_key"]:
                relationship = ListsRelationship()
                relationship.OOR_list = body["oor-list"]
                # relationship.POR_list = body["por-list"]
                session.add(relationship)
                session.commit()
                resp = json.dumps({"Initilization relationship": "successful!"})
                return JSONResponse(content=resp, status_code=200)
            else:
                logging.warning("InitializeRelationship, incorrect Owner or Owner_key ")
                raise HTTPException(status_code=403, detail="Error in Owner parameters")
        else:
            logging.warning("InitializeRelationship(), bad request ")
            raise HTTPException(status_code=400, detail="List already associated")
