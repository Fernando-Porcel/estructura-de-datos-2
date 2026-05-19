from nodo import NodoMvia
from collections import deque


class ArbolMvia:
    """
    Implementa un árbol M-vías.
    
    Atributos:
        _orden (int): El orden del árbol (número máximo de hijos por nodo).
                      El máximo de claves por nodo es orden - 1.
        _raiz (NodoMvia): La raíz del árbol.
    """
    
    def __init__(self, orden):
        """
        Inicializa un nuevo árbol M-vías.
        
        Args:
            orden (int): El orden del árbol. Debe ser al menos 2.
            
        Raises:
            ValueError: Si el orden es menor a 2.
        """
        if orden < 2:
            raise ValueError("El orden debe ser al menos 2")
        
        self._orden = orden
        self._raiz = None

    @property
    def orden(self):
        """
        Obtiene el orden del árbol.
        
        Returns:
            int: El orden del árbol M-vías.
        """
        return self._orden

    @orden.setter
    def orden(self, valor):
        """
        Establece el orden del árbol.
        
        Args:
            valor (int): El nuevo orden del árbol.
        """
        self._orden = valor

    @property
    def raiz(self):
        """
        Obtiene la raíz del árbol.
        
        Returns:
            NodoMvia: El nodo raíz del árbol, o None si el árbol está vacío.
        """
        return self._raiz

    @raiz.setter
    def raiz(self, valor):
        """
        Establece la raíz del árbol.
        
        Args:
            valor (NodoMvia): El nuevo nodo raíz.
        """
        self._raiz = valor

    def buscar(self, clave):
        """
        Busca una clave en el árbol.
        
        Args:
            clave: El valor a buscar.
            
        Returns:
            bool: True si la clave se encuentra en el árbol, False en caso contrario.
        """
        return self._buscar_recursivo(self.raiz, clave)
    
    def _buscar_recursivo(self, nodo, clave):
        """
        Busca recursivamente una clave en el subárbol con raíz en nodo.
        
        Args:
            nodo (NodoMvia): El nodo actual en la búsqueda.
            clave: El valor a buscar.
            
        Returns:
            bool: True si la clave se encuentra, False en caso contrario.
        """
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
        """
        Inserta una nueva clave en el árbol.
        
        Si la clave ya existe, no se realiza la inserción.
        Si el árbol está vacío, crea la raíz.
        
        Args:
            clave: El valor a insertar.
        """
        if self.raiz is None:
            self.raiz = NodoMvia(self.orden)
            self.raiz.claves.append(clave)
            return

        self._insertar_recursivo(self.raiz, clave)
    
    def _insertar_recursivo(self, nodo, clave):
        """
        Inserta recursivamente una clave en el subárbol con raíz en nodo.
        
        Args:
            nodo (NodoMvia): El nodo actual donde se realiza la inserción.
            clave: El valor a insertar.
        """
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1
        
        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return

        if not nodo.esta_lleno():
            nodo.claves.insert(i, clave)
            nodo.hijos.insert(i, None) 
            return
        
        while len(nodo.hijos) <= i:
            nodo.hijos.append(None)

        if nodo.hijos[i] is not None:
            self._insertar_recursivo(nodo.hijos[i], clave)
        else:
            nuevo_hijo = NodoMvia(self.orden)
            nuevo_hijo.claves.append(clave)
            nuevo_hijo.hijos.append(None) 
            nodo.hijos[i] = nuevo_hijo

    def en_orden(self):
        """
        Recorre el árbol en orden.
        
        Realiza un recorrido en orden (izquierda-raíz-derecha) del árbol.
        
        Returns:
            list: Lista de claves en orden.
        """
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        """
        Realiza recursivamente el recorrido en orden.
        
        Args:
            nodo (NodoMvia): El nodo actual.
            resultado (list): Lista acumuladora de claves visitadas.
        """
        if nodo is not None:
            num_claves = len(nodo.claves)

            for i in range(num_claves):
                if i < len(nodo.hijos) and nodo.hijos[i] is not None:
                    self._en_orden(nodo.hijos[i], resultado)
                resultado.append(nodo.claves[i])

            if num_claves < len(nodo.hijos) and nodo.hijos[num_claves] is not None:
                self._en_orden(nodo.hijos[num_claves], resultado)

    def pre_orden(self):
        """
        Recorre el árbol en preorden.
        
        Realiza un recorrido en preorden (raíz-izquierda-derecha) del árbol.
        
        Returns:
            list: Lista de claves en preorden.
        """
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado
    
    def _pre_orden(self, nodo, resultado):
        """
        Realiza recursivamente el recorrido en preorden.
        
        Args:
            nodo (NodoMvia): El nodo actual.
            resultado (list): Lista acumuladora de claves visitadas.
        """
        if nodo is not None:
            num_claves = len(nodo.claves)

            for i in range(num_claves):
                resultado.append(nodo.claves[i])

            for j in range(num_claves):
                if j < len(nodo.hijos) and nodo.hijos[j] is not None:
                    self._pre_orden(nodo.hijos[j], resultado)

            if num_claves < len(nodo.hijos) and nodo.hijos[num_claves] is not None: # <-- Y aquí
                self._pre_orden(nodo.hijos[num_claves], resultado)

    def pos_orden(self):
        """
        Recorre el árbol en posorden.
        
        Realiza un recorrido en posorden (izquierda-derecha-raíz) del árbol.
        
        Returns:
            list: Lista de claves en posorden.
        """
        resultado = []
        self._pos_orden(self.raiz, resultado)
        return resultado

    def _pos_orden(self, nodo, resultado):
        """
        Realiza recursivamente el recorrido en posorden.
        
        Args:
            nodo (NodoMvia): El nodo actual.
            resultado (list): Lista acumuladora de claves visitadas.
        """
        if nodo is not None:
            num_claves = len(nodo.claves)

            for j in range(num_claves):
                if j < len(nodo.hijos) and nodo.hijos[j] is not None:
                    self._pos_orden(nodo.hijos[j], resultado)

            if num_claves < len(nodo.hijos) and nodo.hijos[num_claves] is not None:
                self._pos_orden(nodo.hijos[num_claves], resultado)

            for i in range(num_claves):
                resultado.append(nodo.claves[i])

    def por_nivel(self):
        """
        Recorre el árbol por niveles (en anchura).
        
        Realiza un recorrido por niveles usando una cola (BFS).
        
        Returns:
            list: Lista de niveles, donde cada nivel contiene una lista de claves.
        """
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
        """
        Obtiene la amplitud máxima del árbol.
        
        La amplitud es la cantidad máxima de nodos en un mismo nivel.
        
        Returns:
            int: La amplitud máxima del árbol.
        """
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
        """
        Obtiene la cantidad total de nodos en el árbol.
        
        Returns:
            int: El número total de nodos en el árbol.
        """
        return self._cantidad(self.raiz)
    
    def _cantidad(self, nodo):
        """
        Calcula recursivamente la cantidad de nodos en el subárbol.
        
        Args:
            nodo (NodoMvia): El nodo actual.
            
        Returns:
            int: La cantidad total de nodos en el subárbol.
        """
        if nodo is None:
            return 0
        
        total = 1
        
        for hijo in nodo.hijos:
            total += self._cantidad(hijo)
        
        return total
    
    def altura(self):
        """
        Obtiene la altura del árbol.
        
        La altura es la distancia máxima desde la raíz a cualquier hoja.
        
        Returns:
            int: La altura del árbol (0 si está vacío).
        """
        return self._altura(self.raiz)

    def _altura(self, nodo):
        """
        Calcula recursivamente la altura del subárbol.
        
        Args:
            nodo (NodoMvia): El nodo actual.
            
        Returns:
            int: La altura del subárbol.
        """
        if nodo is None:
            return 0
        
        max_altura = 0

        for hijo in nodo.hijos:
            max_altura = max(max_altura, self._altura(hijo))
        
        return max_altura + 1

    def eliminar(self, clave):
        """
        Elimina una clave del árbol.
        
        Si la clave no existe, no realiza ninguna acción.
        
        Args:
            clave: El valor a eliminar.
        """
        self.raiz = self._eliminar_recursivo(self.raiz, clave)

    def _eliminar_recursivo(self, nodo, clave):
        """
        Elimina recursivamente una clave del subárbol.
        
        Args:
            nodo (NodoMvia): El nodo actual.
            clave: El valor a eliminar.
            
        Returns:
            NodoMvia: El nodo actualizado después de la eliminación.
        """
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
        """
        Obtiene el sucesor (clave más pequeña de la rama derecha).
        
        Args:
            nodo (NodoMvia): El nodo desde donde buscar el sucesor.
            
        Returns:
            El valor de la clave sucesor (la más pequeña de la rama izquierda del hijo).
        """
        while not nodo.es_hoja():
            nodo = nodo.hijos[0]

        return nodo.claves[0]