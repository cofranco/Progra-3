import enum

class EstadoVuelo(enum.Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class TipoUsuario(enum.Enum):
    admin = "admin"
    operador = "operador"
    pasajero = "pasajero"

class Prioridad(enum.Enum):
    alta = 3
    media = 2
    baja = 1
