from fastapi import APIRouter, Request
from vu_interface.control_handlers.set_control import setControl
from vu_interface.control_handlers.status_control import statusControl
from vu_interface.control_handlers.unset_control import unsetControl
from vu_interface.receive_HTTP import manageHTTPcommunication

router = APIRouter()

@router.post('/set-control')
async def set_control(request: Request):
    return setControl.set_control(await request)

@router.post('/check-control-status')
async def check_status(request: Request):
    return statusControl.check_status(await request)

@router.post('/change-control-status')
async def change_status(request: Request):
    return statusControl.change_status(await request)

@router.post('/unset-control')
async def unset_control(request: Request):
    return unsetControl.unset_control(await request)

@router.post('/receive-from-vu')
async def receive_from_vu(request: Request):
    return manageHTTPcommunication.receive_http(await request)
