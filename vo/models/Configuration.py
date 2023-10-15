from config import Base
from sqlalchemy import Column, String

class Configuration(Base):
    __tablename__ ='configuration'
    event = Column(String)
    feature = Column(String)
    permission = Column(String)
    schedulable = Column(String)
    type = Column(String, primary_key=True)
    # device_command = Column(String)
    # flag = Column(String)
    # schedule = Column(String)
