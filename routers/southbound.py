from typing import Annotated
from fastapi import APIRouter, Form, Header, Request
from southbound_api.handlers.initialize import Initialize
from southbound_api.handlers.register import Register
from southbound_api.handlers.send_data import SendData
from southbound_api.handlers.unregister import Unregister
from southbound_api.handlers.feature import Feature
from southbound_api.handlers.clear import Clear
from southbound_api.handlers.delete import Delete

router = APIRouter()

@router.post('/initialize')
async def initialize(request: Request):
    return Initialize.voInfo(await request)

@router.post('/register')
async def register(request: Request):
    r = Register(await request)
    r.check_device()
    r.configuration()
    return "Registration completed"

@router.post('/send-data')
async def send_data(request: Request):
    s = SendData(await request)
    s.validate()
    s.data_input()
    return "Saved Data"

@router.delete('/unregister')
async def unregister(authorization: Annotated[dict | None, Header("Owner key, Unregister key")] = None):
    return Unregister.delete_entity(authorization)

@router.get('/feature-list')
async def feature_list(authorization: Annotated[str | None, Header(description="personal key")] = None):
    return Feature.get_feature_list(authorization)

@router.post('/clear-cache')
async def clear():
    return Clear.clear_cache()

@router.delete('/delete-db')
async def delete():
    return Delete.delete_db()
