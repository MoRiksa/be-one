from fastapi import HTTPException, Request, Response
from models.usersModels import User
from db.session import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
import logging
from fastapi.responses import Response
import bcrypt

# Pengaturan JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2  # Waktu kedaluwarsa token (dalam menit)

# Hashing dan verifikasi password
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Pengaturan logging
logger = logging.getLogger(__name__)


# Fungsi login
async def login(user, db: Session, response: Response):
    logger.info(f"Mencoba login untuk pengguna: {user.email}")
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        logger.warning(f"Percobaan login tidak valid untuk pengguna: {user.email}")
        raise HTTPException(status_code=400, detail="Email atau password tidak valid")

    # Verifikasi password yang di-hash menggunakan bcrypt
    if not bcrypt.checkpw(
        user.password.encode("utf-8"), db_user.hashed_password.encode("utf-8")
    ):
        logger.warning(f"Percobaan login tidak valid untuk pengguna: {user.email}")
        raise HTTPException(status_code=400, detail="Email atau password tidak valid")

    # Menghasilkan token JWT
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": db_user.email, "exp": expire_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Mengatur token JWT sebagai cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=120,  # 2 menit
        secure=True,
        samesite="Strict",
    )

    response.set_cookie(
        key="user_email",
        value=db_user.email,
        max_age=120,  # 2 menit
        secure=True,
        samesite="Strict",
    )

    logger.info(f"Login berhasil untuk pengguna: {user.email}")

    # Return token and email in the response body
    return {"message": "Login berhasil", "token": token, "email": db_user.email}


# Fungsi rute terlindungi (akses token dari cookie)
async def protected_route(request: Request):
    token = request.cookies.get("access_token")  # Mengambil token dari cookie
    if not token:
        logger.error("Token hilang")
        raise HTTPException(status_code=401, detail="Token hilang")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Mengakses rute terlindungi oleh pengguna: {payload['sub']}")
        return {"message": "Ini adalah rute terlindungi", "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        logger.error("Token telah kedaluwarsa")
        raise HTTPException(status_code=401, detail="Token telah kedaluwarsa")
    except jwt.JWTError:
        logger.error("Token tidak valid")
        raise HTTPException(status_code=401, detail="Token tidak valid")


# Fungsi logout
async def logout(response: Response):
    response.delete_cookie("access_token")  # Menghapus cookie token akses
    response.delete_cookie("user_email")  # Opsional menghapus cookie email
    logger.info("Pengguna berhasil logout")
    return {"message": "Logout berhasil"}


# Fungsi registrasi
async def register(user, db: Session):
    try:
        # Periksa apakah pengguna sudah ada berdasarkan email
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            logger.warning(f"Pengguna sudah ada dengan email: {user.email}")
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")

        # Hash password pengguna menggunakan bcrypt
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Buat objek pengguna untuk dimasukkan ke dalam database
        new_user = User(
            email=user.email,
            hashed_password=hashed_password,  # Simpan password yang di-hash
        )

        # Tambahkan pengguna untuk menyimpan ke database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"Pengguna berhasil didaftarkan: {user.email}")
        return {"message": "Pengguna berhasil didaftarkan"}

    except Exception as e:
        logger.error(f"Kesalahan saat mendaftarkan pengguna: {str(e)}")
        raise HTTPException(status_code=500, detail="Kesalahan Internal Server")
