from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.session import get_db
from .schemas import AbsensiCreate, AbsensiUpdate, AbsensiResponse
from .absensi_service import (
    get_all_absensi,
    get_absensi_by_id,
    get_absensi_by_nip,
    checkin_absensi,
    checkout_absensi,
    delete_absensi,
    get_absensi_list_by_nip,
)
from typing import List

absensi_router = APIRouter()


# Endpoint untuk mendapatkan semua absensi
@absensi_router.get("/", response_model=List[AbsensiResponse])
async def get_all_absensi_endpoint(request: Request, db: Session = Depends(get_db)):
    return await get_all_absensi(request, db)


# Endpoint untuk mendapatkan absensi berdasarkan ID
@absensi_router.get("/id/{absensi_id}", response_model=AbsensiResponse)
async def get_absensi_by_id_endpoint(
    request: Request, absensi_id: int, db: Session = Depends(get_db)
):
    return await get_absensi_by_id(request, absensi_id, db)


# Endpoint untuk mendapatkan absensi berdasarkan NIP
@absensi_router.get("/nip/{nip}", response_model=AbsensiResponse)
async def get_absensi_by_nip_endpoint(
    request: Request, nip: str, db: Session = Depends(get_db)
):
    return await get_absensi_by_nip(request, nip, db)


# Endpoint untuk mendapatkan semua absensi berdasarkan NIP
@absensi_router.get("/list/nip/{nip}", response_model=List[AbsensiResponse])
async def get_absensi_list_by_nip_endpoint(
    request: Request, nip: str, db: Session = Depends(get_db)
):
    return await get_absensi_list_by_nip(request, nip, db)


# Endpoint untuk check-in absensi (membuat data baru dengan jam_keluar kosong)
@absensi_router.post("/checkin", response_model=AbsensiResponse)
async def checkin_absensi_endpoint(
    request: Request, absensi: AbsensiCreate, db: Session = Depends(get_db)
):
    return await checkin_absensi(request, absensi, db)


# Endpoint untuk check-out absensi (mengupdate jam_keluar)
@absensi_router.put("/checkout/nip/{nip}", response_model=AbsensiResponse)
async def checkout_absensi_endpoint(
    request: Request,
    nip: str,
    absensi: AbsensiUpdate,
    db: Session = Depends(get_db),
):
    return await checkout_absensi(request, nip, absensi, db)


# Endpoint untuk menghapus absensi berdasarkan ID
@absensi_router.delete("/{absensi_id}", response_model=dict)
async def delete_absensi_endpoint(
    request: Request, absensi_id: int, db: Session = Depends(get_db)
):
    return await delete_absensi(request, absensi_id, db)
