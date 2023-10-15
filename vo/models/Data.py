from config import Base
from sqlalchemy import Column, Integer, String, DateTime

class Data(Base):
    __tablename__ ='Data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feature = Column(String)
    timestamp = Column(DateTime)
    type = Column(String)
    value = Column(String)
