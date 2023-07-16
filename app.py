import uvicorn
from config import app
from routers import northbound, southbound, SVO, vu_interface
from config import session
# import paho.mqtt.client as paho

# def on_message(mosq, obj, msg):
#     print(msg.topic, msg.qos, msg.payload)

#     msg.payload = msg.payload.decode()

#     for key, value in msg.payload:
#         newData = SensorsData(key=value)
#         print(key, value)

#     session.add(newData)
#     session.commit()

#     mosq.publish('pong', 'ack', 0)

# def on_publish(mosq, obj, mid):
#     pass

app.include_router(southbound.router)
app.include_router(northbound.router)
app.include_router(SVO.router)
app.include_router(vu_interface.router)

if __name__ == '__main__':
    uvicorn.run(app)

    # client = paho.Client()
    # client.on_message = on_message
    # client.on_publish = on_publish

    # #client.tls_set('ca.crt', certfile='server.crt', keyfile='server.key')
    # client.connect("127.0.0.1", 1883, 60)

    # client.subscribe("sensors/data", 0)

    # while client.loop() == 0:
    #     pass
