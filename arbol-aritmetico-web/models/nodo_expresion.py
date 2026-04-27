class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None