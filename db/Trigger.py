from config import Base
from sqlalchemy import Column, Integer, String

class Trigger(Base):
    __tablename__ ='trigger'
    triggerId = Column(Integer, primary_key=True)
    appId = Column(String)
    condition = Column(String)
    event = Column(String)
    feature = Column(String)
    output_value = Column(String)
    output_address = Column(String)
    output_method = Column(String)
    status = Column(String)
    value = Column(String)


