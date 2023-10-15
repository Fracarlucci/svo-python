import paho.mqtt.client as paho
import paho.mqtt.publish as publish
from config import session
from vo.models.VoInfo import VoInfo
from vo.models_svo.FriendVoInfo import FriendVoInfo

def on_message(mosq, obj, msg):
    url_rcv = msg.payload.decode()
    print("MES RCV " + msg.topic)

    if url_rcv != "":
        vo_info = session.query(VoInfo).first()

        if msg.topic == vo_info.owner_key:
            OORdiscovery(url_rcv, vo_info)
        elif msg.topic == vo_info.location:
            CLORdiscovery(url_rcv, vo_info)

def on_publish(mosq, obj, mid):
    pass

client = paho.Client()
client.on_message = on_message
client.on_publish = on_publish
client.connect("broker.mqtt-dashboard.com", 1883, 60)

def subscribe_to(topic: str, my_url: str):
    publish.single(topic=topic, payload=my_url, hostname="broker.mqtt-dashboard.com")
    print("Discovery message sent to: " + topic)
    client.subscribe(topic, 0)
    print("Subscribed to: " + topic)
    client.loop_start()

def unsubscribe_from(topic):
    client.unsubscribe(topic)
    print("Unsubscribed from: " + topic)

def OORdiscovery(url_rcv: str, vo_info: VoInfo):
    print(url_rcv)

    friends = session.query(FriendVoInfo).filter_by(relationship="OOR").all()

    for friend in friends:
        if friend.url == url_rcv:
            print("Friend already in db")
            return
    
    new_friend = FriendVoInfo(relationship="OOR", url=url_rcv)
    session.add(new_friend)
    session.commit()

    publish.single(topic=vo_info.owner_key+"/discover", payload=vo_info.url, hostname="broker.mqtt-dashboard.com")

    print("Add new OOR friend")

def CLORdiscovery(url_rcv: str, vo_info: VoInfo):
    print(url_rcv)

    friends = session.query(FriendVoInfo).filter_by(relationship="CLOR").all()

    for friend in friends:
        if friend.url == url_rcv:
            print("Friend already in db")
            return
    
    new_friend = FriendVoInfo(relationship="CLOR", url=url_rcv)
    session.add(new_friend)
    session.commit()

    publish.single(topic=vo_info.location+"/discover", payload=vo_info.url, hostname="broker.mqtt-dashboard.com")

    print("Add new CLOR friend")