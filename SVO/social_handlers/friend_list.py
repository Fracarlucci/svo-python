from fastapi import HTTPException, Request
from vo.models_svo.Friend_OOR import FriendOOR
from northbound_api.functions import Functions
import logging


class GetFriendList():
    def get_friends(key : str):
        # body = request.form
        user_data = {}
        user_data['key'] = key
        mandatory = ["key"]
        Functions.check_mandatory_parameters(Functions(), mandatory, user_data)
        level = Functions.get_permission_level(Functions(), user_data['key'])
        if level == "owner":
            list_friends = FriendOOR.query.all()
            for friend in list_friends:
                return friend.friend_OOR
        else:
            logging.warning("GetFriendList, get_friends() method. Wrong key")
            raise HTTPException(status_code=400, detail="Bad request. Please check key parameter")
