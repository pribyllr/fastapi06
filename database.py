import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

load_dotenv()

# Read DB_USER and DB_PASS from environment variables
DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/fastapi_module6_2".format(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base class
class Base(DeclarativeBase):
    pass

Base.metadata.create_all(bind=engine)

# Dependency for FastAPI routes
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()