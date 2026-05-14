from nodo import NodoMvia
from collections import deque

class ArbolMvia:
    def __init__(self, orden):
        self.orden = orden
        self.raiz = None

    def buscar(self, clave):
        return self._buscar_recursivo(self.raiz, clave)
    
    def _buscar_recursivo(self, nodo, clave):
        if nodo is None:
            return False
        
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return True
        
        if nodo.es_hoja():
            return False
        
        return self._buscar_recursivo(nodo.hijos[i], clave)

    def insertar(self, clave):
        if self.raiz is None:
            self.raiz = NodoMvia(self.orden)
            self.raiz.claves.append(clave)
            return

        self._insertar_recursivo(self.raiz, clave)
    
    def _insertar_recursivo(self, nodo, clave):
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1
        
        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return

        if not nodo.esta_lleno():
            nodo.claves.insert(i, clave)
            return
        
        if nodo.hijos[i] is None:
            nodo.hijos[i] = NodoMvia(self.orden)
            nodo.hijos[i].claves.append(clave)
            return

        self._insertar_recursivo(nodo.hijos[i], clave)

    def en_orden(self):
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        if nodo is not None:
            num_claves = len(nodo.claves)

            for i in range(num_claves):
                if nodo.hijos[i] is not None:
                    self._en_orden(nodo.hijos[i], resultado)
                resultado.append(nodo.claves[i])

            self._en_orden(nodo.hijos[num_claves], resultado)

    def pre_orden(self):
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado
    
    def _pre_orden(self, nodo, resultado):
        if nodo is not None:
            num_claves = len(nodo.claves)

            for i in range(num_claves):
                resultado.append(nodo.claves[i])

            for j in range(num_claves):
                if nodo.hijos[j] is not None:
                    self._pre_orden(nodo.hijos[j], resultado)

            self._pre_orden(nodo.hijos[num_claves], resultado)

    def pos_orden(self):
        resultado = []
        self._pos_orden(self.raiz, resultado)
        return resultado

    def _pos_orden(self, nodo, resultado):
        if nodo is not None:
            num_claves = len(nodo.claves)

            for j in range(num_claves):
                if nodo.hijos[j] is not None:
                    self._pos_orden(nodo.hijos[j], resultado)

            self._pos_orden(nodo.hijos[num_claves], resultado)

            for i in range(num_claves):
                resultado.append(nodo.claves[i])

    def por_nivel(self):
        if self.raiz is None:
            return []
        
        resultado = []
        cola = deque([self.raiz])

        while cola:
            nivel_actual = []

            for _ in range(len(cola)):
                nodo = cola.popleft()
                nivel_actual.append(nodo.claves[:])

                for hijo in nodo.hijos:
                    if hijo is not None:
                        cola.append(hijo)

            resultado.append(nivel_actual)

        return resultado
    
    def amplitud(self):
        if self.raiz is None:
            return 0
        
        cola = deque([self.raiz])
        max_amplitud = 0

        while cola:
            longitud = len(cola)
            max_amplitud = max(max_amplitud, longitud)

            for _ in range(longitud):
                nodo = cola.popleft()

                for hijo in nodo.hijos:
                    if hijo is not None:
                        cola.append(hijo)

        return max_amplitud
    
    def cantidad(self):
        return self._cantidad(self.raiz)
    
    def _cantidad(self, nodo):
        if nodo is None:
            return 0
        
        total = 1
        
        for hijo in nodo.hijos:
            total += self._cantidad(hijo)
        
        return total
    
    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        
        max_altura = 0

        for hijo in nodo.hijos:
            max_altura = max(max_altura, self._altura(hijo))
        
        return max_altura + 1

    def eliminar(self, clave):
        self.raiz = self._eliminar_recursivo(self.raiz, clave)

    def _eliminar_recursivo(self, nodo, clave):
        if nodo is None:
            return None

        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and nodo.claves[i] == clave:
            if nodo.es_hoja():
                nodo.claves.pop(i)

                if len(nodo.claves) == 0:
                    return None

                return nodo

            sucesor = self._obtener_sucesor(nodo.hijos[i + 1])
            nodo.claves[i] = sucesor
            nodo.hijos[i + 1] = self._eliminar_recursivo(nodo.hijos[i + 1], sucesor)

            return nodo

        nodo.hijos[i] = self._eliminar_recursivo(nodo.hijos[i], clave)

        return nodo
    
    def _obtener_sucesor(self, nodo):
        while not nodo.es_hoja():
            nodo = nodo.hijos[0]

        return nodo.claves[0]