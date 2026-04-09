from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PlantBase(BaseModel):
    species_name: str
    common_name: Optional[str] = None
    family: str
    habitat: str
    max_height_cm: Optional[int] = None
    flowering_season: Optional[str] = None

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True   # SQLAlchemy model se Pydantic model banane ke liye