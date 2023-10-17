import paho.mqtt.client as paho
import paho.mqtt.publish as publish
from config import session
from vo.models.VoInfo import VoInfo
from vo.models_svo.FriendVoInfo import FriendVoInfo

def on_message(mosq, obj, msg):
    url_rcv = msg.payload.decode()
    vo_info = session.query(VoInfo).first()

    if url_rcv != "" and url_rcv != vo_info.url:
        suffix = "/discover"
        OORtopic = vo_info.owner_key + suffix
        CLORtopic = vo_info.location + suffix
        
        print("New message in " + msg.topic)

        if msg.topic == OORtopic:
            friend_discovery(url_rcv, OORtopic, "OOR", vo_info.url)
        elif msg.topic == CLORtopic:
            friend_discovery(url_rcv, CLORtopic, "CLOR", vo_info.url)

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

def friend_discovery(url_rcv: str, topic: str, relationship: str, my_url: str):
    friends = session.query(FriendVoInfo).filter_by(relationship=relationship).all()

    for friend in friends:
        if friend.url == url_rcv and friend.relationship == relationship:
            print("You and {} are already friends".format(url_rcv))
            return
    
    new_friend = FriendVoInfo(relationship=relationship, url=url_rcv)
    session.add(new_friend)
    session.commit()

    publish.single(topic=topic, payload=my_url, hostname="broker.mqtt-dashboard.com")

    print("Added new {} friend: {}".format(relationship, url_rcv))
