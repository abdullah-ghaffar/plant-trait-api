from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import engine, get_db, Base
from models import Plant as PlantModel   # ← yahan alias laga diya (sabse important line)
from schemas import PlantCreate, Plant

# Tables create kar do
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plant Trait Database API",
    description="Biology students ke liye Plant Species aur Traits ka REST API",
    version="1.0"
)

# ==================== ENDPOINTS ====================

@app.get("/plants", response_model=List[Plant])
def get_all_plants(db: Session = Depends(get_db)):
    plants = db.query(PlantModel).all()
    return plants

@app.post("/plants", response_model=Plant)
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = PlantModel(**plant.model_dump())   # ab yeh SQLAlchemy model use ho raha hai
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

@app.get("/plants/{plant_id}", response_model=Plant)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(PlantModel).filter(PlantModel.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.put("/plants/{plant_id}", response_model=Plant)
def update_plant(plant_id: int, updated_plant: PlantCreate, db: Session = Depends(get_db)):
    plant = db.query(PlantModel).filter(PlantModel.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    for key, value in updated_plant.model_dump().items():
        setattr(plant, key, value)
    
    db.commit()
    db.refresh(plant)
    return plant

@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(PlantModel).filter(PlantModel.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    db.delete(plant)
    db.commit()
    return {"message": "Plant deleted successfully"}

# Bonus Biology Feature: Habitat wise search
@app.get("/plants/habitat/{habitat_name}", response_model=List[Plant])
def get_plants_by_habitat(habitat_name: str, db: Session = Depends(get_db)):
    plants = db.query(PlantModel).filter(PlantModel.habitat.ilike(f"%{habitat_name}%")).all()
    return plants


# Optional: Root endpoint (sirf testing ke liye)
@app.get("/")
def root():
    return {"message": "🌱 Plant Trait Database API is running! Go to /docs"}