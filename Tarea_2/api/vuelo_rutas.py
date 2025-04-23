from fastapi import APIRouter, HTTPException
from estructuras.vuelo_schema import VueloCreate
from models.vuelo import Vuelo
from api.vuelo_api import VueloAPI
from db.conexion import session
from enums.enums import EstadoVuelo

router = APIRouter()
api = VueloAPI(session)

@router.post("/vuelos")
def crear_vuelo(vuelo_data: VueloCreate):
    vuelo = Vuelo(**vuelo_data.dict())
    vuelo_guardado = api.insertar_vuelo(vuelo)
    return {"mensaje": "Vuelo insertado", "vuelo": str(vuelo_guardado)}

@router.get("/vuelos")
def obtener_vuelos():
    return [str(v) for v in api.recorrer_lista()]

@router.get("/vuelos/proximo")
def obtener_proximo():
    vuelo = api.obtener_proximo()
    return {"vuelo": str(vuelo)} if vuelo else {"mensaje": "No hay vuelos"}

@router.delete("/vuelos/{pos}")
def eliminar_vuelo(pos: int):
    vuelo = api.extraer_de_posicion(pos)
    if vuelo:
        return {"mensaje": "Vuelo eliminado", "vuelo": str(vuelo)}
    raise HTTPException(status_code=404, detail="Posición inválida")

@router.put("/vuelos/reordenar")
def reordenar_vuelos(pos_origen: int, pos_destino: int):
    vuelo = api.reordenar_vuelos(pos_origen, pos_destino)
    if vuelo:
        return {"mensaje": "Vuelo movido", "vuelo": str(vuelo)}
    raise HTTPException(status_code=404, detail="Posiciones inválidas")

@router.get("/vuelos/estado/{estado}")
def filtrar_por_estado(estado: EstadoVuelo):
    vuelos_filtrados = [str(v) for v in api.recorrer_lista() if v.estado == estado]
    return {"vuelos": vuelos_filtrados}
