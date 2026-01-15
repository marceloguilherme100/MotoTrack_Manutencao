from sqlalchemy import Column, Integer, String
from database import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    moto = Column(String)
    part_name = Column(String)
    last_change_km = Column(Integer)
    current_km = Column(Integer)
    life_km = Column(Integer)
