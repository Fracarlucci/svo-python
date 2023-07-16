from config import Base
from sqlalchemy import Column, String

class Device_Id(Base):
    __tablename__ = 'device_Id'
    hal_key = Column(String, primary_key=True)
