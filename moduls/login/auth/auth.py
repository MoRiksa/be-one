from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from moduls.login.auth.auth_service import login, protected_route, logout, register
from db.session import get_db
from .schemas import UserLogin, UserRegister

auth_router = APIRouter()


# Login endpoint
@auth_router.post("/login")
async def login_route(
    user: UserLogin, db: Session = Depends(get_db), response: Response = None
):
    return await login(user, db, response)


# Protected route (ambil token dari cookie)
@auth_router.get("/protected")
async def protected_route_route(request: Request):
    return await protected_route(request)


# Logout endpoint
@auth_router.post("/logout")
async def logout_route(response: Response):
    return await logout(response)


@auth_router.post("/register")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    # Panggil fungsi register untuk menambah user baru
    return await register(user, db)
