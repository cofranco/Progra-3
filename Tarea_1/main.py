from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import modelos, esquema
from base_ import SessionLocal, engine

# inicializa las tablas
modelos.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/personajes", response_model=esquema.Personaje)
def crear_personaje(personaje: esquema.PersonajeCreate, db: Session = Depends(get_db)):
    nuevo = modelos.Personaje(nombre=personaje.nombre, experiencia=0)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.post("/misiones", response_model=esquema.Mision)
def crear_mision(mision: esquema.MisionCreate, db: Session = Depends(get_db)):
    nueva_mision = modelos.Mision(
        descripcion=mision.descripcion,
        recompensa_xp=mision.recompensa_xp
    )
    db.add(nueva_mision)
    db.commit()
    db.refresh(nueva_mision)
    return nueva_mision


@app.post("/personajes/{personaje_id}/misiones/{mision_id}", response_model=esquema.Personaje)
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    personaje = db.query(modelos.Personaje).filter(modelos.Personaje.id == personaje_id).first()
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    mision = db.query(modelos.Mision).filter(modelos.Mision.id == mision_id).first()
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    if not any(m.id == mision.id for m in personaje.misiones):  # Se mejoró la validación
        personaje.misiones.append(mision)
        db.commit()
        db.refresh(personaje)

    return personaje


@app.post("/personajes/{id}/completar", response_model=esquema.Personaje)
def completar_mision(id: int, db: Session = Depends(get_db)):
    personaje = db.query(modelos.Personaje).filter(modelos.Personaje.id == id).first()

    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    if not personaje.misiones:
        raise HTTPException(status_code=400, detail="No hay misiones para completar")

    mision = personaje.misiones[0]
    personaje.experiencia += mision.recompensa_xp
    personaje.misiones.remove(mision)

    db.commit()
    db.refresh(personaje)
    return personaje


@app.delete("/misiones/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mision(id: int, db: Session = Depends(get_db)):
    mision = db.query(modelos.Mision).filter(modelos.Mision.id == id).first()

    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    
    for personaje in mision.personajes:
        personaje.misiones.remove(mision)

    db.delete(mision)
    db.commit()
    return


@app.delete("/personajes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_personaje(id: int, db: Session = Depends(get_db)):
    personaje = db.query(modelos.Personaje).filter(modelos.Personaje.id == id).first()

    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    
    personaje.misiones = []

    db.delete(personaje)
    db.commit()
    return

# para correr el servidor
# uvicorn main:app --reload
# http://127.0.0.1:8000/docs