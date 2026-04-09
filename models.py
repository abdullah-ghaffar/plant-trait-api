from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base
import datetime

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    species_name = Column(String, unique=True, index=True, nullable=False)
    common_name = Column(String, index=True)
    family = Column(String, index=True)
    habitat = Column(String, index=True)
    max_height_cm = Column(Integer)
    flowering_season = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())