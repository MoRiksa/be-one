from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    email: str
    id_role: int

    class Config:
        orm_mode = True
        from_attributes = True


class UserUpdate(BaseModel):
    email: str
    id_role: int

    class Config:
        orm_mode = True
        from_attributes = True
