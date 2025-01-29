from fastapi import HTTPException, Request, Response
from models.models import User
from db.session import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
import logging
from fastapi.responses import Response
import bcrypt

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiration time (in minutes)

# Password hashing and verification
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Logging setup
logger = logging.getLogger(__name__)


# Login function
async def login(user, db: Session, response: Response):
    logger.info(f"Attempting login for user: {user.email}")
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        logger.warning(f"Invalid login attempt for user: {user.email}")
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verifikasi password yang di-hash menggunakan bcrypt
    if not bcrypt.checkpw(
        user.password.encode("utf-8"), db_user.hashed_password.encode("utf-8")
    ):
        logger.warning(f"Invalid login attempt for user: {user.email}")
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate JWT token
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": db_user.email, "exp": expire_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Set the JWT token as an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,  # 1 hour
        secure=True,
        samesite="Strict",
    )

    # Set the email as a non-HttpOnly cookie (this allows JavaScript access to it)
    response.set_cookie(
        key="user_email",
        value=db_user.email,
        max_age=3600,  # 1 hour
        secure=True,
        samesite="Strict",
    )

    logger.info(f"Login successful for user: {user.email}")
    return {"message": "Login successful"}


# Protected route function (access token from cookies)
async def protected_route(request: Request):
    token = request.cookies.get("access_token")  # Retrieve the token from the cookies
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Accessing protected route by user: {payload['sub']}")
        return {"message": "This is a protected route", "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        logger.error(f"Token expired for user: {token}")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        logger.error(f"Invalid token attempt: {token}")
        raise HTTPException(status_code=401, detail="Invalid token")


# Logout function
async def logout(response: Response):
    response.delete_cookie("access_token")  # Remove the access token cookie
    response.delete_cookie("user_email")  # Optionally remove the email cookie
    logger.info("User logged out")
    return {"message": "Logout successful"}


async def register(user, db: Session):
    # Check if the user already exists by email
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"User already exists with email: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the user's password using bcrypt
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # Create the user object to insert into the database
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,  # Store the hashed password
    )

    # Add the user to the session and commit to save to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User registered successfully: {user.email}")
    return {"message": "User registered successfully"}
