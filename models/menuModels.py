from sqlalchemy import Column, Integer, String, Float
from db.db_config import Base


class Menu(Base):
    __tablename__ = "menu"

    id_menu = Column(Integer, primary_key=True, index=True)
    nama_menu = Column(String, index=True)
    harga = Column(Float)
    id_kategori = Column(Integer)


class Kategori(Base):
    __tablename__ = "kategori"

    id_kategori = Column(Integer, primary_key=True, index=True)
    nama_kategori = Column(String, nullable=False, index=True)
