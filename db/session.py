# db_session.py
from db.db_config import SessionLocal  # Importing the sessionmaker from db_config
from sqlalchemy.orm import Session
from typing import Generator


# Function to get the database session
def get_db() -> Generator[Session, None, None]:  # Correcting the return type
    db = SessionLocal()  # Opening a new session
    try:
        yield db  # Yielding the session
    finally:
        db.close()  # Closing the session after use
