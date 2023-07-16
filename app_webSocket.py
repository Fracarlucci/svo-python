from datetime import datetime
import json
import uvicorn
from config import app
from routers import southbound as southbound
from routers import northbound as northbound
from config import session, Base, engine
import vo.models.SensorsData as db
import socketio

app.include_router(southbound.router)
app.include_router(northbound.router)
# app.include_router(SVO.router)
# app.include_router(vu_interface.router)

@app.get('/live-sensors-data-websocket/')
async def get_live_sensor_data():
    return await sio.emit(event="read_sensors")

sio = socketio.AsyncServer(async_mode='asgi')

app = socketio.ASGIApp(sio, app)

io = socketio.Server(ping_timeout=10000, ping_interval=10)

@sio.event
async def add_sensors_data(sid, sensors):
    sensorsData = json.loads(sensors)
    print(sensorsData)
    
    acceleration = db.Acceleration(x=sensorsData["acceleration"][0], y=sensorsData["acceleration"][1], z=sensorsData["acceleration"][2])
    newData = db.SensorsData(dateTime=datetime.now(), acceleration=acceleration, accelerationId=acceleration.id,
                             pressure=sensorsData["pressure"], temperature=sensorsData["temperature"],
                             humidity=sensorsData["humidity"], battery_percentage=sensorsData["battery_percentage"])
    session.add(newData)
    session.commit()

    print("Data added to database")

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    uvicorn.run(app, host="192.168.1.8", port=80)
