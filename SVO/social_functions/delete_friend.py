from fastapi import Request
from config import session
from vo.models_svo.FriendVoInfo import FriendVoInfo
from vo.models_svo.Friend_OOR import FriendOOR
from vo.models_svo.Friend_POR import FriendPOR
from vo.models_svo.Friend_CLOR import FriendCLOR

class DeleteFriend():
    def delete_friend(svo_url : str):
        # body = request.get_json(force=True)
        url_to_delete = svo_url
        print(url_to_delete)
        if FriendVoInfo.query.filter(FriendVoInfo.url == url_to_delete).first() is not None:
            a = FriendVoInfo.query.filter(FriendVoInfo.url == url_to_delete).first()
            session.delete(a)
            session.commit()
        if FriendOOR.query.filter(FriendOOR.friend_OOR == url_to_delete).first() is not None:
            a = FriendOOR.query.filter(FriendOOR.friend_OOR == url_to_delete).first()
            session.delete(a)
            session.commit()
        if FriendCLOR.query.filter(FriendCLOR.friend_CLOR == url_to_delete).first() is not None:
            a = FriendCLOR.query.filter(FriendCLOR.friend_CLOR == url_to_delete).first()
            session.delete(a)
            session.commit()
        if FriendPOR.query.filter(FriendPOR.friend_POR == url_to_delete).first() is not None:
            a = FriendPOR.query.filter(FriendPOR.friend_POR == url_to_delete).first()
            session.delete(a)
            session.commit()



