from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file folder mein hi banega
SQLALCHEMY_DATABASE_URL = "sqlite:///./plant_traits.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite ke liye zaroori
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency jo har request ke liye database session dega
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()