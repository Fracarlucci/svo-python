import paho.mqtt.client as paho
from config import session
import vo.models.SensorsData as db
from datetime import datetime
import json

def on_message(mosq, obj, msg):
    msg.payload = msg.payload.decode()

    sensorsData = json.loads(msg.payload)
    print(sensorsData)

    acceleration = db.Acceleration(x=sensorsData["acceleration"][0], y=sensorsData["acceleration"][1], z=sensorsData["acceleration"][2])
    newData = db.SensorsData(dateTime=datetime.now(), acceleration=acceleration, accelerationId=acceleration.id,
                             pressure=sensorsData["pressure"], temperature=sensorsData["temperature"],
                             humidity=sensorsData["humidity"], battery_percentage=sensorsData["battery_percentage"])

    session.add(newData)
    session.commit()

    print("Data added to database")

def on_publish(mosq, obj, mid):
    pass

def set_up_mqtt(hal_key: str):
    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect("broker.mqtt-dashboard.com", 1883, 60)
    client.subscribe(hal_key + "/post-sensors", 0)
    client.loop_start()
