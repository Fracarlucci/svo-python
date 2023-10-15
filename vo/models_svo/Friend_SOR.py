from config import Base
from sqlalchemy import Column, Integer, String

class FriendSOR(Base):
    __tablename__ = 'friendSOR'
    friend_SOR = Column(String)
    id = Column(Integer, primary_key=True, autoincrement=True)
    friend_tag = Column(String)