import json
from vo.models.VoInfo import VoInfo
from vo.models_svo.Friend_CLOR import FriendCLOR
from vo.models_svo.Friend_SOR import FriendSOR
import config
from datetime import datetime
import requests
class ReceiveMessage():
    def receive_mqtt_message(self, msg):
        if "svo_url" in msg.keys():
            vo = VoInfo.query.first()
            if vo.url == msg["svo_url"]:
                print("Its me!!")
            else:
                if msg["class"]=="fixed" and vo.location == 'fixed':
                    if FriendCLOR.query.filter_by(friend_CLOR=str(msg["svo_url"])).first() is None:
                        param = {"svo_url": vo.url, "type": "CLOR"}##TAG???#
                        url_rec_friend = str(msg['vo_url']) + "receive/friendship/request"
                        payload = json.dumps(param)
                        requests.post(url_rec_friend, data=payload)

                else: ##mobile, oppure fixed ma non è fixed chi lo riceve
                    # if msg["tag"]=="mobile":
                    n_meetings = str(('n_meetings_') + msg["svo_url"])
                    actual_meetings = 1
                    if config.cache.get(n_meetings) is None:
                        now = datetime.now()
                        now_dt = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
                        config.cache.set(n_meetings, {"n": actual_meetings, "time": now_dt})
                    else:##Possono essere registrate diverse SOR da postazioni diverse ## DA SVILUPPARE
                        mettings = config.cache.get(n_meetings)
                        actual_meetings = mettings["n"]
                        print(actual_meetings)
                        if config.min_n_meetings == actual_meetings:
                            print("possiamo diventare amici")
                            #if FriendSOR.query.filter_by(friend_SOR=str(msg["vo_url"])).first() is None:
                            ReceivedRequest= ('ReceivedRequest') + "_"+ str(msg["svo_url"]) + "_" + str(msg["place"])
                            if config.cache.get(ReceivedRequest) == "True":
                                #Salva profilo
                                param = {"svo_url": vo.url, "type": "SOR", "tag": msg["place"]}
                                url_rec_friend = str(msg['svo_url']) + "receive/friendship/request"
                                payload = json.dumps(param)
                                requests.post(url_rec_friend, data=payload)
                                SentRequest = ('SentRequest') + "_"+ str(msg["svo_url"]) + "_" + str(msg["place"])
                                config.cache.set(SentRequest, "True")
                                FriendProfile.share_profile(FriendProfile(), body)
                                FriendProfile.update_friends_db(FriendProfile(), body)
                            else:
                                #Non lo salva ancora
                                param = {"svo_url": vo.url, "type": "SOR", "tag": msg["place"]}
                                url_rec_friend = str(msg['svo_url']) + "receive/friendship/request"
                                payload = json.dumps(param)
                                requests.post(url_rec_friend, data=payload)
                                SentRequest = ('SentRequest') + "_" + str(msg["svo_url"]) + "_" + str(msg["place"])
                                config.cache.set(SentRequest, "True")

                        else:
                            at_istant = mettings["time"]
                            now = datetime.now()
                            now_dt = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
                            print(at_istant, now_dt)
                            diff_dt = now_dt - at_istant
                            if (int(diff_dt.days) > 0):
                                print("è passato oltre un giorno, incrementa conteggio")
                                actual_meetings = actual_meetings + 1
                                config.cache.set(n_meetings, {"n":actual_meetings, "time":at_istant})
                            else:
                                if (float(diff_dt.seconds / 60)) >0:
                                    print("sono passati almeno cinque minuti, incrementa il conteggio")
                                    actual_meetings = actual_meetings + 1
                                    config.cache.set(n_meetings,{"n":actual_meetings, "time":at_istant})
                                else:
                                    print("non è passato abbastaza tempo!")
                    print(str(config.cache.get(n_meetings)))
        else:
            print("thi message cannot be use.")
            print(msg)












