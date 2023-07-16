import uvicorn
from config import app
from routers import southbound as southbound
from routers import northbound as northbound
import json
import uvicorn
from config import session, app
import vo.models.SensorsData as db
from datetime import datetime
import paho.mqtt.client as paho

app.include_router(southbound.router)
app.include_router(northbound.router)
# app.include_router(SVO.router)
# app.include_router(vu_interface.router)

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

if __name__ == '__main__':

    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    #client.tls_set('ca.crt', certfile='server.crt', keyfile='server.key')
    client.connect("broker.mqtt-dashboard.com", 1883, 60)
    client.subscribe("sensors/post_data", 0)
    client.loop_start()

    uvicorn.run(app, host="192.168.1.8", port=80)
