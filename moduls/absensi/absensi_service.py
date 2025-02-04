from sqlalchemy.orm import Session
from models.absensiModels import Absensi
from .schemas import AbsensiCreate, AbsensiUpdate, AbsensiResponse
from fastapi import HTTPException
import logging

# Logging setup
logger = logging.getLogger(__name__)


async def get_all_absensi(db: Session):
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


async def get_absensi_by_id(absensi_id: int, db: Session):
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


async def checkin_absensi(absensi: AbsensiCreate, db: Session):
    try:
        new_absensi = Absensi(**absensi.dict())
        db.add(new_absensi)
        db.commit()
        db.refresh(new_absensi)
        logger.info(f"Checked in absensi record for NIP {absensi.nip}")
        return AbsensiResponse.from_orm(new_absensi)
    except Exception as e:
        logger.error(f"Error checking in absensi record: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def checkout_absensi(absensi_id: int, absensi_update: AbsensiUpdate, db: Session):
    try:
        absensi = db.query(Absensi).filter(Absensi.id == absensi_id).first()
        if not absensi:
            logger.warning(f"Absensi record with ID {absensi_id} not found")
            raise HTTPException(status_code=404, detail="Absensi not found")
        absensi.jam_keluar = absensi_update.jam_keluar
        db.commit()
        db.refresh(absensi)
        logger.info(f"Checked out absensi record with ID {absensi_id}")
        return AbsensiResponse.from_orm(absensi)
    except Exception as e:
        logger.error(f"Error checking out absensi record: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def delete_absensi(absensi_id: int, db: Session):
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
