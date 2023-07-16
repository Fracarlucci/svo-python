from config import Base
from sqlalchemy import Column, Integer, String

class Control(Base):
    __tablename__ ='control'
    controlID = Column(Integer, primary_key  =True, autoincrement  =True)
    condition = Column(String)
    event = Column(String)
    feature = Column(String)
    status = Column(String)
    value = Column(String)
