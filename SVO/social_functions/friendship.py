from fastapi import HTTPException, Request
from vo.models.VoInfo import VoInfo
import config
from config import session
import requests, json
from vo.models_svo.Friend_OOR import FriendOOR
from vo.models_svo.Friend_CLOR import FriendCLOR
from vo.models_svo.Friend_POR import FriendPOR
from vo.models_svo.Friend_SOR import FriendSOR
from vo.models_svo.FriendVoInfo import FriendVoInfo
from vo.models_svo.ListsRelationship import ListsRelationship
import logging
from northbound_api.functions import Functions
from SVO.utils.send_request_back import send_it_back

class SendFriendshipRequest():

    async def send():
        # if request is not None:
        #     body = await request.json()
        #     print(body)
        #recupera liste da VoInfo
        LR = session.query(ListsRelationship).first()
        list_vo_OOR = LR.OOR_list
        ##eventuali tags che si vogliono aggiugere
        #list_vo_POR = LR.POR_list #arrivano da piattaforma - POSTMAN per test
        ###DA PIATTAFORMA ARRIVA ANCHE OWNER_KEY - già lo fa
        VO = session.query(VoInfo).first()

        # recupero url di questo VO che invia la richiesta di amicizia
        url_vo_sender = VO.url
        owner_key = VO.owner_key

        # invio richiesta amicizia agli altri VO
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
        for url in list_vo_OOR:
            if session.query(FriendOOR).filter_by(friend_OOR=str(url["svo_url"])).first()  is None: # FriendOOR.query.filter_by(friend_OOR= str(url["svo_url"])).first()
                param = {"svo_url": url_vo_sender, "type": "OOR", "owner_key": owner_key}
                # handler che elabora la richiesta"
                url_rec_friend = str(url['svo_url']) + "receive-friendship-request"
                print(url_rec_friend)
                payload = json.dumps(param)
                requests.post(url_rec_friend, data=payload)
            else:
                return "Already friends"

        #for url in list_vo_POR:
            #param = {"svo_url": url_vo_sender, "type": "POR"}
            # handler che elabora la richiesta
            #url_rec_friend = str(url['svo_url']) + "/receive/friendship/request"
            #payload = json.dumps(param)
            #requests.post(url_rec_friend, data=payload)

class ReceiveFriendshipRequest():

    async def receive(request : Request):
        # ricevo url del VO che richiede amicizia
        #body = request.json
        body = await request.json()
        print(body)
        # recupero mio url e invio richiesta
        VO = session.query(VoInfo).first()
        owner_key = VO.owner_key
        my_url = VO.url
        mandatory = ["svo_url",
                     "type"]
        Functions.check_mandatory_parameters(Functions(), mandatory, body)
        if body["type"]=="OOR":
            mandatory = ["owner_key",
                         "svo_url",
                         "type"]
            Functions.check_mandatory_parameters(Functions(), mandatory, body)
            if owner_key == body["owner_key"]:
                # recupero mio url e invio richiesta prova
                print(my_url)
                send_it_back(my_url=my_url, body=body)
                FriendProfile.share_profile(FriendProfile(),body)
            else:
                logging.warning("Friendship, ReceiveFriendshipRequest, receive(). Wrong owner_key.")
                raise HTTPException(status_code=400, detail="Wrong owner_key.")
        if body["type"] == "CLOR":
            mandatory = ["svo_url",
                         "type"]
            Functions.check_mandatory_parameters(Functions(), mandatory, body)
            send_it_back(my_url=my_url, body=body)
            FriendProfile.share_profile(FriendProfile(), body)
            FriendProfile.update_friends_db(FriendProfile(),body)

        if body["type"] == "SOR":
            mandatory = ["svo_url",
                         "type"]
            Functions.check_mandatory_parameters(Functions(), mandatory, body)
            ###send_it_back(my_url=my_url, body=body)
            ###FriendProfile.share_profile(FriendProfile(), body) 09/11
            #### non lo fa in automatico??? 09/11 FriendProfile.update_friends_db(FriendProfile(),body)
            # ReceivedRequest = ('ReceivedRequest') + "_" + str(msg["svo_url"]) + "_" + str(msg["place"])



class ReceiveFriendshipBack():

    async def receive_back(request : Request):
        body = await request.json()
        # ricevo url del VO che ha risposto all'amicizia
        mandatory = ["type",
                     "svo_url"]
        Functions.check_mandatory_parameters(Functions(), mandatory, body)
        print(body)
        # salvo nella tabella amicizie il suo url
        FriendProfile.update_friends_db(FriendProfile(), body)
        FriendProfile.share_profile(FriendProfile(), body)




class FriendProfile():

    def get_profile(body : dict):
        # body = json.dumps(friend)
        item = FriendVoInfo()
        item.type = body["type"]
        if "w_mac" in body.keys():
            item.w_mac = body["w_mac"]

        if "b_mac" in body.keys():
            item.b_mac = body["b_mac"]

        ##item.hal_key = body["hal_key"] ?? ma c'è o no
        item.brand = body["brand"]
        item.model = body["model"]
        item.owner = body["owner"]
        #vo_info.owner_key = body["owner_key"]
        item.url = body["url"]
        item.friend_key = body["friend_key"]
        item.location = body["location"]
        item.latitude = body["latitude"]
        item.longitude = body["longitude"]
        item.model = body ["model"]
        #vo_info.unregister_key = body["unregister_key"]
        session.add(item)
        session.commit()

    def share_profile(self,body):
        VO = VoInfo.query.first()
        param = {"w_mac": VO.w_mac, "type": body["type"], "brand": VO.brand, "b_mac": VO.b_mac, "friend_key": VO.friend_key, "location":VO.location, "latitude":VO.latitude,
                 "longitude": VO.longitude, "location_name": VO.location_name, "location_range": VO.location_range, "model": VO.model, "owner":VO.owner, "url":VO.url
                 }
        url_rec_friend = str(body["svo_url"] + "get-friend-profile")
        payload = json.dumps(param)
        requests.post(url_rec_friend, data=payload)

    def update_friends_db(self, body):
        friend_url = body["svo_url"]
        if body["type"] == "OOR":
            finally_friend = FriendOOR()
            finally_friend.friend_OOR = friend_url
            if "tag" in body.keys():
                finally_friend.friend_tag=body["tag"]
            session.add(finally_friend)
            session.commit()
            #FriendProfile.share_profile(FriendProfile(), body)
        if body["type"] == "CLOR":
            finally_friend = FriendCLOR()
            finally_friend.friend_CLOR = friend_url
            if "tag" in body.keys():
                finally_friend.friend_tag=body["tag"]
            session.add(finally_friend)
            session.commit()
            #FriendProfile.share_profile(FriendProfile(), body)
        if body["type"] == "SOR":
            finally_friend = FriendSOR()
            finally_friend.friend_SOR = friend_url
            if "tag" in body.keys():
                finally_friend.friend_tag=body["tag"]
            session.add(finally_friend)
            session.commit()
            #FriendProfile.share_profile(FriendProfile(), body)

        else:
            finally_friend = FriendPOR()
            finally_friend.friend_POR = friend_url
            if "tag" in body.keys():
                finally_friend.friend_tag=body["tag"]
            session.add(finally_friend)
            session.commit()
            #FriendProfile.share_profile(FriendProfile(), body)















