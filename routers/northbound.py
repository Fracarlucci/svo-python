import datetime
from typing import Annotated
from fastapi import APIRouter, Header, Request
import paho.mqtt.publish as publish
from config import session
from northbound_api.handlers.get_schedule import GetSchedule
from northbound_api.handlers.set_schedule import SetSchedule
from northbound_api.handlers.set_trigger import SetTrigger
from northbound_api.handlers.status_trigger import StatusTrigger
from northbound_api.handlers.unset_trigger import UnsetTrigger
from northbound_api.handlers.sensor import GetSensor
from northbound_api.handlers.actuator import SetActuator

router = APIRouter()

@router.post('/actuator')
async def set_actuator_status(request: Request):
   return SetActuator(await request).granted_actions()

@router.get('/schedule/{feature}') # GET
async def get_schedule(feature : str):
    return GetSchedule(feature).granted_actions()

@router.get('/sensors/') # HEADER
async def get_sensor(sensor: Annotated[dict | None, Header("Sensor info")] = None):
    return GetSensor(sensor).granted_actions()

@router.get('/live-sensors-data-mqtt/')
async def get_live_sensor_data():
    return publish.single(topic="sensors/get_data", hostname="broker.mqtt-dashboard.com")

@router.post('/set-schedule')
async def set_schedule(request: Request):
    return SetSchedule(await request).granted_actions()

@router.post('/set-trigger')
async def set_trigger(request: Request):
    return SetTrigger(await request).granted_actions()

@router.get('/trigger') # HEADER
async def get_trigger_status(trigger: Annotated[dict | None, Header("Trigger info")] = None):
    return StatusTrigger(trigger).granted_actions()

@router.delete('/trigger') # HEADER
async def unset_trigger(trigger: Annotated[dict | None, Header("Trigger info")] = None):
    return UnsetTrigger(trigger).granted_actions()
