from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Ambil URL database dari environment variable untuk keamanan
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:admin@localhost/latihandata"
)

# Set up database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk model
Base = declarative_base()
