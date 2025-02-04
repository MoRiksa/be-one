from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.session import get_db
from .schemas import AbsensiCreate, AbsensiUpdate, AbsensiResponse
from .absensi_service import (
    get_all_absensi,
    get_absensi_by_id,
    checkin_absensi,
    checkout_absensi,
    delete_absensi,
)
from typing import List

absensi_router = APIRouter()


# Endpoint untuk mendapatkan semua absensi
@absensi_router.get("/", response_model=List[AbsensiResponse])
async def get_all_absensi_endpoint(db: Session = Depends(get_db)):
    return await get_all_absensi(db)


# Endpoint untuk mendapatkan absensi berdasarkan ID
@absensi_router.get("/{absensi_id}", response_model=AbsensiResponse)
async def get_absensi_by_id_endpoint(absensi_id: int, db: Session = Depends(get_db)):
    return await get_absensi_by_id(absensi_id, db)


# Endpoint untuk check-in absensi (membuat data baru dengan jam_keluar kosong)
@absensi_router.post("/checkin", response_model=AbsensiResponse)
async def checkin_absensi_endpoint(
    absensi: AbsensiCreate, db: Session = Depends(get_db)
):
    return await checkin_absensi(absensi, db)


# Endpoint untuk check-out absensi (mengupdate jam_keluar)
@absensi_router.put("/checkout/{absensi_id}", response_model=AbsensiResponse)
async def checkout_absensi_endpoint(
    absensi_id: int, absensi: AbsensiUpdate, db: Session = Depends(get_db)
):
    return await checkout_absensi(absensi_id, absensi, db)


# Endpoint untuk menghapus absensi berdasarkan ID
@absensi_router.delete("/{absensi_id}", response_model=dict)
async def delete_absensi_endpoint(absensi_id: int, db: Session = Depends(get_db)):
    return await delete_absensi(absensi_id, db)
