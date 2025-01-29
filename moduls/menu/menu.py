from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.session import get_db
from .schemas import MenuResponse, respondKategori, MenuCreate, MenuUpdate
from .menu_service import (
    get_all_menus,
    get_menus_with_category,
    create_menu,
    update_menu,
    delete_menu,
    get_menu_by_id,
)
from typing import List

menu_router = APIRouter()


# Endpoint untuk mendapatkan daftar menu
@menu_router.get("/", response_model=List[MenuResponse])
async def get_menu(request: Request, db: Session = Depends(get_db)):
    return await get_all_menus(request, db)


# Endpoint untuk mendapatkan menu dengan kategori
@menu_router.get(
    "/menu-kategori",
    summary="Get Menu dengan Kategori",
    description="Mengambil semua item menu beserta kategorinya",
    response_model=respondKategori,
)
async def get_menu_with_category(db: Session = Depends(get_db)):
    return await get_menus_with_category(db)


# Endpoint untuk membuat menu baru
@menu_router.post("/", response_model=MenuResponse)
async def create_menu_endpoint(menu: MenuCreate, db: Session = Depends(get_db)):
    return await create_menu(menu, db)


# Endpoint untuk memperbarui menu berdasarkan ID
@menu_router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu_endpoint(
    menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)
):
    return await update_menu(menu_id, menu, db)


# Endpoint untuk menghapus menu berdasarkan ID
@menu_router.delete("/{menu_id}", response_model=dict)
async def delete_menu_endpoint(menu_id: int, db: Session = Depends(get_db)):
    return await delete_menu(menu_id, db)


# Endpoint untuk mendapatkan menu berdasarkan ID
@menu_router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu_by_id_endpoint(menu_id: int, db: Session = Depends(get_db)):
    return await get_menu_by_id(menu_id, db)
