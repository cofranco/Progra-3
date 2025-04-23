from sqlalchemy.orm import Session
from models.vuelo import Vuelo
from datetime import datetime

class VueloAPI:
    def __init__(self, db: Session):
        self.db = db

    def insertar_vuelo(self, vuelo: Vuelo):
        session = self.db() 
        vuelo.orden = session.query(Vuelo).count() 
        session.add(vuelo)
        session.commit() 
        session.refresh(vuelo)
        session.close() 
        return vuelo

    def obtener_total(self):
        session = self.db()  
        total_vuelos = session.query(Vuelo).count()
        session.close() 
        return total_vuelos

    def obtener_proximo(self):
        session = self.db() 
        vuelo_proximo = session.query(Vuelo).filter(Vuelo.hora >= datetime.now()).order_by(Vuelo.hora.asc()).first()
        session.close()  
        return vuelo_proximo

    def obtener_ultimo(self):
        session = self.db() 
        vuelo_ultimo = session.query(Vuelo).order_by(Vuelo.hora.desc()).first()
        session.close() 
        return vuelo_ultimo

    def extraer_de_posicion(self, pos):
        session = self.db()  
        vuelos = session.query(Vuelo).order_by(Vuelo.orden.asc()).all()
        if 0 <= pos < len(vuelos):
            vuelo = vuelos[pos]
            session.delete(vuelo)
            session.commit()
            self._reordenar_orden(session) 
            session.close()  
            return vuelo
        session.close() 
        return None

    def recorrer_lista(self):
        session = self.db() 
        vuelos = session.query(Vuelo).order_by(Vuelo.orden.asc()).all()
        session.close() 
        return vuelos

    def reordenar_vuelos(self, pos_origen, pos_destino):
        session = self.db()  # Obtienes la sesión
        vuelos = session.query(Vuelo).order_by(Vuelo.orden.asc()).all()
        if 0 <= pos_origen < len(vuelos) and 0 <= pos_destino < len(vuelos):
            vuelo = vuelos.pop(pos_origen)
            vuelos.insert(pos_destino, vuelo)
            for i, v in enumerate(vuelos):
                v.orden = i
            session.commit() 
            session.close()  
            return vuelo
        session.close() 
        return None

    def _reordenar_orden(self, session):
        vuelos = session.query(Vuelo).order_by(Vuelo.orden.asc()).all()
        for i, vuelo in enumerate(vuelos):
            vuelo.orden = i
        session.commit()  
