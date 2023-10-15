from config import Base
from sqlalchemy import Column, Integer, String

class FriendCLOR(Base):
    __tablename__ = 'friendCLOR'
    id = Column(Integer, primary_key=True, autoincrement=True)
    friend_CLOR = Column(String)
    friend_tag = Column(String)
