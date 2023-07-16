from config import Base
from sqlalchemy import Column, Integer, String

class VoInfo(Base):
    __tablename__= 'voInfo'
    brand = Column(String)
    b_mac = Column(String)
    friend_key = Column(String)
    location = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    location_name = Column(String)
    location_range = Column(String)
    model = Column(String)
    owner_key = Column(String, primary_key=True)
    owner = Column(String)
    url = Column(String)
    w_mac = Column(String)
    unregister_key= Column(String)
    vu_url = Column(String)
