from fastapi import FastAPI
from db.db_config import Base, engine
from moduls.login.auth.auth import auth_router
from moduls.menu.menu import menu_router
from starlette.middleware.cors import CORSMiddleware
from logging_config import setup_logging

# Setup logging
setup_logging()

# FastAPI initialization
app = FastAPI()

# CORS middleware setup
origins = [
    "http://localhost:3000",  # Pastikan ini adalah alamat dari frontend Anda
    # Anda bisa menambahkan lebih banyak alamat jika dibutuhkan
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Izinkan asal tertentu saja
    allow_credentials=True,  # Izinkan kredensial untuk dikirim
    allow_methods=["*"],  # Izinkan semua metode HTTP
    allow_headers=["*"],  # Izinkan semua header
)

# Include the auth router
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(menu_router, prefix="/menu", tags=["Menu"])

# Create tables in the database
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
