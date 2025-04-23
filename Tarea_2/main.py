# main.py
from fastapi import FastAPI
# from api import vuelo_api  
from api.vuelo_rutas import router as vuelo_router
from db.conexion import Base, engine

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

from api.vuelo_rutas import router as vuelo_router

app = FastAPI()

# Incluir las rutas
app.include_router(vuelo_router)


# from db.conexion import session
# from estructuras.lista_vuelos import ListaVuelos
# from api.vuelo_api import VueloAPI
# from models.vuelo import Vuelo
# from enums.enums import EstadoVuelo
# from datetime import datetime



# para correr el servidor
# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
