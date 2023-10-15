from typing import Annotated
from fastapi import APIRouter, Form, Header, Request
from southbound_api.handlers.initialize import Initialize
from southbound_api.handlers.register import Register
from southbound_api.handlers.update_vo_info import UpdateVoInfo
from southbound_api.handlers.send_data import SendData
from southbound_api.handlers.unregister import Unregister
from southbound_api.handlers.feature import Feature
from southbound_api.handlers.clear import Clear
from southbound_api.handlers.delete import Delete

router = APIRouter()

@router.post('/initialize')
async def initialize(request: Request):
    return await Initialize.voInfo(request)

@router.post('/register')
async def register(request: Request):
    r = await Register.create(request)
    await r.check_device()
    await r.configuration()
    return "Registration completed"

@router.post('/update-vo-info')
async def update_vo_info(request: Request):
    return await UpdateVoInfo.update_vo_info(request)

@router.post('/send-data')
async def send_data(request: Request):
    s = SendData(await request)
    s.validate()
    s.Data_input()
    return "Saved Data"

# @router.delete('/unregister')
# async def unregister(authorization: Annotated[dict | None, Header("Owner key, Unregister key")] = None):
#     return Unregister.delete_entity(authorization)

@router.get('/feature-list')
async def feature_list(authorization: Annotated[str | None, Header(description="personal key")] = None):
    return Feature.get_feature_list(authorization)

@router.post('/clear-cache')
async def clear():
    return Clear.clear_cache()

@router.delete('/delete-db')
async def delete():
    return Delete.delete_db()
