from config import Base
from sqlalchemy import Column, Integer, String

class FriendPOR(Base):
    __tablename__ = 'friendPOR'
    friend_POR = Column(String)
    id = Column(Integer, primary_key=True, autoincrement=True)
    friend_tag = Column(String)