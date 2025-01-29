from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from models.menuModels import Menu, Kategori
from .schemas import MenuResponse, respondKategori, MenuCreate, MenuUpdate
from jose import jwt
import logging

# Logging setup
logger = logging.getLogger(__name__)

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"


# Fungsi untuk memverifikasi token
def verify_token(request: Request):
    token = request.cookies.get("access_token")  # Mengambil token dari cookies
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Fungsi untuk mendapatkan semua menu
async def get_all_menus(request: Request, db: Session):
    user = verify_token(request)  # Memverifikasi token
    menus = db.query(Menu).all()  # Mengambil semua data menu dari database
    if not menus:
        raise HTTPException(status_code=404, detail="Menu not found")

    logger.info(f"User {user} retrieved all menus")
    return menus


# Fungsi untuk mendapatkan menu dengan kategori
async def get_menus_with_category(db: Session):
    try:
        # Mengambil data hasil join antara Menu dan Kategori
        menukategori = (
            db.query(Menu, Kategori.nama_kategori)
            .join(Kategori, Menu.id_kategori == Kategori.id_kategori)
            .all()
        )

        if not menukategori:
            raise HTTPException(
                status_code=404, detail="Menu dengan Kategori Tidak Ada"
            )

        response_data = [
            {
                "id_menu": item.Menu.id_menu,
                "nama_menu": item.Menu.nama_menu,
                "harga": item.Menu.harga,
                "id_kategori": item.Menu.id_kategori,
                "nama_kategori": item[1],
            }
            for item in menukategori
        ]

        logger.info(f"Menampilkan Daftar Menu dengan Kategori {response_data}")

        # Mengembalikan response dengan schema yang sesuai
        return respondKategori(
            status="success",
            message="Menampilkan Daftar Menu dengan Kategori",
            data=response_data,
        )

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Terjadi Kesalahan: {str(e)}")


# Fungsi untuk membuat menu baru
async def create_menu(menu: MenuCreate, db: Session):
    try:
        # validasi apakah menu sudah ada
        menu_tersedia = db.query(Menu).filter(Menu.nama_menu == menu.nama_menu).first()
        if menu_tersedia:
            raise HTTPException(status_code=400, detail="Menu Sudah Ada")

        # Menambahkan menu baru ke database
        new_menu = Menu(
            id_menu=menu.id_menu,
            nama_menu=menu.nama_menu,
            harga=menu.harga,
            id_kategori=menu.id_kategori,
        )
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)

        logger.info(f"Menu created: {new_menu.nama_menu}")
        return new_menu

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Fungsi untuk memperbarui menu berdasarkan ID
async def update_menu(menu_id: int, menu: MenuUpdate, db: Session):
    db_menu = db.query(Menu).filter(Menu.id_menu == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    for key, value in menu.dict().items():
        setattr(db_menu, key, value)

    db.commit()
    db.refresh(db_menu)
    logger.info(f"Menu updated: {db_menu.nama_menu}")
    return db_menu


# Fungsi untuk menghapus menu berdasarkan ID
async def delete_menu(menu_id: int, db: Session):
    db_menu = db.query(Menu).filter(Menu.id_menu == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    db.delete(db_menu)
    db.commit()
    logger.info(f"Menu deleted: {db_menu.nama_menu}")
    return {"message": "Menu deleted successfully"}


# Fungsi untuk mendapatkan menu berdasarkan ID
async def get_menu_by_id(menu_id: int, db: Session):
    menu = db.query(Menu).filter(Menu.id_menu == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    logger.info(f"Menu retrieved: {menu.nama_menu}")
    return menu
