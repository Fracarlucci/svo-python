import socket
import uvicorn
from config import session, Base, engine, app
from routers import southbound, northbound, SVO
import uvicorn
from vo.models.Device_Id import Device_Id
from vo.models.VoInfo import VoInfo
import SVO.utils.svo_mqtt_comm as mqtt_comm
import device_comm

app.include_router(southbound.router)
app.include_router(northbound.router)
app.include_router(SVO.router)
# app.include_router(vu_interface.router)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    device = session.query(Device_Id).first()
    vo_info = session.query(VoInfo).first()

    if device != None and vo_info != None:
        device_comm.set_up_mqtt(device.hal_key)
        mqtt_comm.subscribe_to(vo_info.owner_key + "/discover", vo_info.url)
        mqtt_comm.subscribe_to(vo_info.location + "/discover", vo_info.url)

    uvicorn.run(app, host=socket.gethostbyname(socket.gethostname()), port=80) # 192.168.1.2
