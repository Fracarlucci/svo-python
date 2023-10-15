from vo.models.VoInfo import VoInfo
from fastapi import HTTPException, Request
from config import session
import logging
import SVO.utils.svo_mqtt_comm as mqtt_comm

class Initialize:
    
    async def voInfo(request : Request):
        body = await request.json()
        print(body)
        try:
            if (body["owner"] == '' or body["owner_key"] == ''
                or body["unregister_key"] == '' or body["url"] == ''): # body["friend_key"] == ''
                raise HTTPException(status_code=400, detail="Missing parameters")
            else:
                vo_info = VoInfo(owner = body["owner"], owner_key = body["owner_key"],
                                 unregister_key = body["unregister_key"], url = body["url"])
                                # friend_key = body["friend_key"], vu_url = body["vu_url"])
                session.add(vo_info)
                session.commit()

                # OOR relationship
                mqtt_comm.subscribe_to(body["owner_key"] + "/discover", vo_info.url)

                return "Initialization success!!"
        except Exception:
            logging.warning("Initialize, error in initialization in svo.")
            raise HTTPException(status_code=400, detail="Bad request. Error in initialization!")
