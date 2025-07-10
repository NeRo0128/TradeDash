from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases import Database
import os

# Database URL
DATABASE_URL = "sqlite:///./data/tradedash.db"

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database instance for async operations
database = Database(DATABASE_URL)

# Base class for SQLAlchemy models
Base = declarative_base()