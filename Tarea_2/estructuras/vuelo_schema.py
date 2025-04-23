from pydantic import BaseModel
from datetime import datetime
from enums.enums import EstadoVuelo

class VueloCreate(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str

class VueloCreate(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str