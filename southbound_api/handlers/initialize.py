from db.VoInfo import VoInfo
from fastapi import HTTPException, Request
from config import session
import logging

class Initialize:
    
    def voInfo(self, request : Request):
        body = request.json()
        try:
            if body["owner"] == '' or body["vu_url"]== '' or body["owner_key"] == '' or body["friend_key"] == '' or body["url"] == '' or body["unregister_key"] == '':
                raise HTTPException(status_code=400, detail="Missing parameters")
            else:
                vo_info = VoInfo(owner = body["owner"], owner_key = body["owner_key"],
                                 url = body["url"], friend_key = body["friend_key"],
                                 unregister_key = body["unregister_key"], vu_url = body["vu_url"])
                session.add(vo_info)
                session.commit()
                return "Initialization success!!"
        except Exception:
            logging.warning("Initialize, error in initialization in svo.")
            raise HTTPException(status_code=400, detail="Bad request. Error in initialization!")
