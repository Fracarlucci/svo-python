from config import Base
from sqlalchemy import Column, Integer, JSON

class ListsRelationship(Base):
    __tablename__ = 'ListsRelationship'
    id_list = Column(Integer, primary_key=True, autoincrement=True)
    OOR_list = Column(JSON)
    POR_list = Column(JSON)
    SOR_list = Column(JSON)
    CWORK_list = Column(JSON)
    CLOR_list = Column(JSON)
