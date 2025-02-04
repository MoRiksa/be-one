from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.session import get_db
from .schemas import UserResponse, UserUpdate
from .users_service import get_all_users, delete_user, update_user
from typing import List

users_router = APIRouter()


# Endpoint untuk mendapatkan semua pengguna
@users_router.get("/", response_model=List[UserResponse])
async def get_all_users_endpoint(db: Session = Depends(get_db)):
    return await get_all_users(db)


# Endpoint untuk menghapus pengguna berdasarkan ID
@users_router.delete("/{user_id}", response_model=dict)
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return await delete_user(user_id, db)


# Endpoint untuk memperbarui pengguna berdasarkan ID
@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(
    user_id: int, user: UserUpdate, db: Session = Depends(get_db)
):
    return await update_user(user_id, user, db)
