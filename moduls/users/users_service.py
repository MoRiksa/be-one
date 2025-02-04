from sqlalchemy.orm import Session
from models.usersModels import User
from .schemas import UserResponse, UserUpdate
from fastapi import HTTPException


async def get_all_users(db: Session):
    users = db.query(User).all()
    return [UserResponse.from_orm(user) for user in users]


async def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


async def update_user(user_id: int, user_update: UserUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return UserResponse.from_orm(user)
