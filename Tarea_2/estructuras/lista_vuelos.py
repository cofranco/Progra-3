from estructuras.nodo import Nodo

class ListaVuelos:
    def __init__(self, session):
        self.cabeza = None
        self.cola = None
        self.size = 0
        self.session = session

    def insertar_al_frente(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        self.size += 1

    def insertar_al_final(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.cola:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.size += 1

    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None

    def longitud(self):
        return self.size

    def insertar_en_posicion(self, vuelo, pos):
        if pos <= 0:
            self.insertar_al_frente(vuelo)
        elif pos >= self.size:
            self.insertar_al_final(vuelo)
        else:
            actual = self.cabeza
            for _ in range(pos):
                actual = actual.siguiente
            nuevo = Nodo(vuelo)
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo
            self.size += 1

    def extraer_de_posicion(self, pos):
        if pos < 0 or pos >= self.size:
            return None
        actual = self.cabeza
        for _ in range(pos):
            actual = actual.siguiente
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.cabeza = actual.siguiente
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        else:
            self.cola = actual.anterior
        self.size -= 1
        return actual.vuelo
