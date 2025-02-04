from pydantic import BaseModel, validator
from datetime import datetime, time
from typing import Optional


class AbsensiBase(BaseModel):
    nip: str
    jam_masuk: time
    jam_keluar: Optional[time] = None
    tanggal: datetime

    @validator("jam_masuk", "tanggal", pre=True, always=True)
    def validate_datetime(cls, value):
        if value is None:
            raise ValueError("Field cannot be None")
        return value


class AbsensiCreate(AbsensiBase):
    pass


class AbsensiUpdate(BaseModel):
    jam_keluar: time


class AbsensiResponse(AbsensiBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
