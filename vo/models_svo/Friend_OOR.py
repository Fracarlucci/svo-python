from config import Base
from sqlalchemy import Column, Integer, String

class FriendOOR(Base):
    __tablename__ = 'friendOOR'
    id = Column(Integer, primary_key=True, autoincrement=True)
    friend_OOR = Column(String)
    friend_tag = Column(String)
