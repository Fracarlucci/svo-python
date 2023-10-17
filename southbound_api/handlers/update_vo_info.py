from config import session
from fastapi import HTTPException, Request
from vo.models.VoInfo import VoInfo
import SVO.utils.svo_mqtt_comm as mqtt_comm

class UpdateVoInfo:

    async def update_vo_info(request : Request):
        body = await request.json()
        vo_info = session.query(VoInfo).first()
        
        # Update CLOR relationship
        if "location" in body:
            mqtt_comm.unsubscribe_from(vo_info.location)
            mqtt_comm.subscribe_to(body["location"] + "/discover", vo_info.url)

        for key, value in body.items():
            setattr(vo_info, key, value)
        session.commit()

        return "update VoInfo success!!"
    