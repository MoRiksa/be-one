from sqlalchemy.orm import Session
from models.absensiModels import Absensi
from .schemas import AbsensiCreate, AbsensiUpdate, AbsensiResponse
from fastapi import HTTPException, Request
import logging
from datetime import date

# Logging setup
logger = logging.getLogger(__name__)


async def get_all_absensi(request: Request, db: Session):
    access_token = request.cookies.get("access_token")
    user_email = request.cookies.get("user_email")
    try:
        absensi_list = db.query(Absensi).all()
        if not absensi_list:
            logger.warning("No absensi records found")
            raise HTTPException(status_code=404, detail="No absensi records found")
        logger.info("Retrieved all absensi records")
        return [AbsensiResponse.from_orm(absensi) for absensi in absensi_list]
    except Exception as e:
        logger.error(f"Error retrieving all absensi records: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_absensi_by_id(request: Request, absensi_id: int, db: Session):
    access_token = request.cookies.get("access_token")
    user_email = request.cookies.get("user_email")
    try:
        absensi = db.query(Absensi).filter(Absensi.id == absensi_id).first()
        if not absensi:
            logger.warning(f"Absensi record with ID {absensi_id} not found")
            raise HTTPException(status_code=404, detail="Absensi not found")
        logger.info(f"Retrieved absensi record with ID {absensi_id}")
        return AbsensiResponse.from_orm(absensi)
    except Exception as e:
        logger.error(f"Error retrieving absensi record by ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_absensi_by_nip(request: Request, nip: str, db: Session):
    access_token = request.cookies.get("access_token")
    user_email = request.cookies.get("user_email")
    try:
        if not nip:
            logger.warning("Invalid request: NIP is undefined or empty")
            raise HTTPException(status_code=400, detail="NIP is required")

        absensi = db.query(Absensi).filter(Absensi.nip == nip).first()

        if not absensi:
            logger.warning(f"Absensi record with NIP {nip} not found")
            raise HTTPException(
                status_code=404, detail=f"Absensi with NIP {nip} not found"
            )

        logger.info(f"Retrieved absensi record with NIP {nip}")
        return AbsensiResponse.from_orm(absensi)
    except Exception as e:
        logger.error(f"Error retrieving absensi record by NIP {nip}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def checkin_absensi(request: Request, absensi: AbsensiCreate, db: Session):
    access_token = request.cookies.get("access_token")
    user_email = request.cookies.get("user_email")
    try:
        new_absensi = Absensi(
            nip=absensi.nip, jam_masuk=absensi.jam_masuk, tanggal=absensi.tanggal
        )
        db.add(new_absensi)
        db.commit()
        db.refresh(new_absensi)
        logger.info(f"Checked in absensi record for NIP {absensi.nip}")
        return AbsensiResponse.from_orm(new_absensi)
    except Exception as e:
        logger.error(f"Error checking in absensi record: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def checkout_absensi(
    request: Request, nip: str, absensi_update: AbsensiUpdate, db: Session
):
    access_token = request.cookies.get("access_token")
    user_email = request.cookies.get("user_email")
    try:
        today = date.today()
        absensi = (
            db.query(Absensi)
            .filter(
                Absensi.nip == nip, Absensi.jam_keluar == None, Absensi.tanggal == today
            )
            .first()
        )
        if not absensi:
            logger.warning(
                f"Absensi record with NIP {nip} not found or already checked out for today"
            )
            raise HTTPException(
                status_code=404,
                detail="Absensi not found or already checked out for today",
            )
        absensi.jam_keluar = absensi_update.jam_keluar
        db.commit()
        db.refresh(absensi)
        logger.info(f"Checked out absensi record with NIP {nip} for today")
        return AbsensiResponse.from_orm(absensi)
    except Exception as e:
        logger.error(
            f"Error checking out absensi record by NIP {nip} for today: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def delete_absensi(request: Request, absensi_id: int, db: Session):
    access_token = request.cookies.get("access_token")
    user_email = request.cookies.get("user_email")
    try:
        absensi = db.query(Absensi).filter(Absensi.id == absensi_id).first()
        if not absensi:
            logger.warning(f"Absensi record with ID {absensi_id} not found")
            raise HTTPException(status_code=404, detail="Absensi not found")
        db.delete(absensi)
        db.commit()
        logger.info(f"Deleted absensi record with ID {absensi_id}")
        return {"message": "Absensi deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting absensi record: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
