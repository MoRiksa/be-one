from sqlalchemy import Column, Integer, String, DateTime, Time
from db.db_config import Base


class Absensi(Base):
    __tablename__ = "log_absensi"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nip = Column(String, index=True, nullable=False)
    jam_masuk = Column(Time, nullable=False)
    jam_keluar = Column(Time, nullable=True)
    tanggal = Column(DateTime, nullable=False)
