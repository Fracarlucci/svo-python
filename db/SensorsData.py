from config import Base
from sqlalchemy import Column, ForeignKey, Float, Integer, DateTime
from sqlalchemy.orm import backref, relationship

class SensorsData(Base):
    __tablename__ = 'sensorsData'
    id = Column(Integer, primary_key=True)
    dateTime = Column(DateTime)
    pressure = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    battery_percentage = Column(Float)

    accelerationId = Column(Integer, ForeignKey('acceleration.id'))
    acceleration = relationship("Acceleration", backref=backref("sensorsData", uselist=False))

class Acceleration(Base):
    __tablename__ = 'acceleration'
    id = Column(Integer, primary_key=True)

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    