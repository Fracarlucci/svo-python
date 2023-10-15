import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException, Header, Request
from SVO.social_functions.friendship import *
from SVO.social_functions.delete_friend import DeleteFriend
from SVO.social_handlers.friend_list import GetFriendList
from SVO.social_handlers.initialize_relationship import InitializeRelationship

router = APIRouter()

@router.post('/initialize-relationship')
async def initialize_relationship(request : Request):
    return await InitializeRelationship.initialize_relationship(request)

@router.post('/send-friendship-request')
async def send_friendship_request():
    try:
        return await SendFriendshipRequest.send()
    except Exception:
        logging.warning(" Send_friendship_request, error in send")
        raise HTTPException(status_code=400, detail="Error in send")

@router.post('/receive-friendship-request')
async def receive_friendship_request(request : Request):
    try:
        await ReceiveFriendshipRequest.receive(request)
        return "request receive"
    except Exception:
        logging.warning("Receive_friendship_request, error in receive")
        raise HTTPException(status_code=400, detail="Error in receive")

@router.post('/receive-friendship-back')
async def receive_friendship_back(request : Request):
    try:
        await ReceiveFriendshipBack.receive_back(request)
        return "request receive back"
    except Exception:
        logging.warning("Receive_friendship_back, error in receive back")
        raise HTTPException(status_code=400, detail="Error in receive back")

# @router.get('/friends/') # HEADER
# async def get_friend_profile(friend: Annotated[dict | None, Header("Friend info")] = None):
#     try:
#         FriendProfile.get_profile(friend)
#         return "Profile sent"
#     except Exception:
#         logging.warning("FriendProfile, error in get_friend_profile")
#         raise HTTPException(status_code=400, detail="Error in get friend profile")

@router.get('/friendList') # HEADER
async def get_friend_list(authorization: Annotated[str | None, Header(description="personal key")] = None):
    return GetFriendList.get_friends(authorization)

@router.delete('/friend') # HEADER
async def delete_friend_info(authorization: Annotated[str | None, Header(description="url to delete")] = None):
    try:
        DeleteFriend.delete_friend(authorization)
        return "Done"
    except Exception:
        logging.warning("DeleteFriend method. Error in delete database")
        raise HTTPException(status_code=400, detail="Impossible to delete")
