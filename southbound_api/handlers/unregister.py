from fastapi import HTTPException, Request
from vo.models_svo.FriendVoInfo import FriendVoInfo
from db.VoInfo import VoInfo
import config
import json, requests
from config import session

class Unregister:
    
    def delete_entity(self, header_val : dict):
        header = header_val
        u_key = header["unregister_key"]
        o_key = header["owner_key"]
        if "unregister_key" in header.keys() and "owner_key" in header.keys():

            if session.query(VoInfo).filter_by(unregister_key=u_key).first() is None or session.query(VoInfo).filter_by(owner_key=o_key).first() is None:
                raise HTTPException(status_code=400, detail='Wrong unregister_key or wrong Owner_key')
            else:
                f = session.query(FriendVoInfo).query.all()
                vo = session.query(FriendVoInfo).first()
                url=vo.url
                #Tutti gli amici devono cancellare le sue informazioni
                for i in f:
                    friend_url = i.url + "friend/delete"
                    param = {"vo_url": url}
                    payload = json.dumps(param)
                    requests.post(friend_url, data=payload)
                meta = session.metadata
                for table in reversed(meta.sorted_tables):
                    session.execute(table.delete())
                    session.commit()
                config.cache.clear()
                return "Clean"
        else:
            raise HTTPException(status_code=400, detail='Missing unregister_key or owner_key')
