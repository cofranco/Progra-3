from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from base_ import Base

class Personaje(Base):
    __tablename__ = "Personaje"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, index=True)
    experiencia = Column(Integer, nullable=False, default=0)  # Añadido `default=0`
    misiones = relationship("Mision", secondary="Relacion", back_populates="personajes")

class Mision(Base):
    __tablename__ = "Mision"
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(250), nullable=False)
    recompensa_xp = Column(Integer, nullable=False)
    personajes = relationship("Personaje", secondary="Relacion", back_populates="misiones")
    
Relacion = Table(
    "Relacion", Base.metadata,
    Column("personaje_id", ForeignKey("Personaje.id"), primary_key=True),
    Column("mision_id", ForeignKey("Mision.id"), primary_key=True)
) 