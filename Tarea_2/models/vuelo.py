from sqlalchemy import Column, String, Enum, DateTime, Integer
from db.conexion import Base
from enums.enums import EstadoVuelo

class Vuelo(Base):
    __tablename__ = 'vuelos'

    codigo = Column(String, primary_key=True)
    estado = Column(Enum(EstadoVuelo), nullable=False)
    hora = Column(DateTime, nullable=False)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    orden = Column(Integer, nullable=False)  # Nuevo campo

    def __repr__(self):
        return f"<Vuelo {self.codigo} - {self.origen} -> {self.destino} ({self.estado.name})>"
