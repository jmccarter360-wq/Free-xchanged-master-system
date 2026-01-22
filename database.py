from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database configuration
DATABASE_URL = "sqlite:///./test.db"  # Update this URL for other databases

# Create an engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our classes definitions
Base = declarative_base()

# Dependency to get the session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()