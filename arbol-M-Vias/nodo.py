class NodoMvia:
    def __init__(self, orden):
        self.orden = orden
        self.claves = []
        self.hijos = [None] * orden

    def es_hoja(self):
        return all(hijo is None for hijo in self.hijos)

    def esta_lleno(self):
        return len(self.claves) >= self.orden - 1