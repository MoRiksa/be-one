from pydantic import BaseModel
from typing import List


# Schema untuk membaca data menu
class MenuBase(BaseModel):
    nama_menu: str
    harga: float
    id_kategori: int


# Schema untuk membuat menu baru
class MenuCreate(MenuBase):
    id_menu: int


# Schema untuk memperbarui menu
class MenuUpdate(MenuBase):
    pass


# Schema untuk membaca data menu dengan ID (response model)
class MenuResponse(MenuBase):
    id_menu: int

    class Config:
        orm_mode = True


class KategoriItem(BaseModel):
    id_menu: int
    nama_menu: str
    harga: float
    id_kategori: int
    nama_kategori: str

    class Config:
        orm_mode = True
        from_attributes = True


class respondKategori(BaseModel):
    status: str
    message: str
    data: List[KategoriItem]

    class Config:
        orm_mode = True
        from_attributes = True


class respondDetail(BaseModel):
    status: str
    message: str
    data: KategoriItem

    class Config:
        orm_mode = True
        from_attributes = True
