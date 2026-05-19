class NodoMvia:
    """
    Representa un nodo en un árbol M-vías.
    
    Atributos:
        _orden (int): El orden del árbol al cual pertenece este nodo.
        _claves (list): Lista de valores (claves) almacenados en el nodo.
        _hijos (list): Lista de referencias a nodos hijos (puede contener None).
    """
    
    def __init__(self, orden):
        """
        Inicializa un nuevo nodo M-vías.
        
        Args:
            orden (int): El orden del árbol M-vías al que pertenece este nodo.
                        Determina la capacidad máxima de claves (orden - 1).
        """
        self._orden = orden
        self._claves = []
        self._hijos = []

    @property
    def orden(self):
        """
        Obtiene el orden del nodo.
        
        Returns:
            int: El orden del árbol M-vías.
        """
        return self._orden

    @orden.setter
    def orden(self, valor):
        """
        Establece el orden del nodo.
        
        Args:
            valor (int): El nuevo valor del orden.
        """
        self._orden = valor

    @property
    def claves(self):
        """
        Obtiene la lista de claves almacenadas en el nodo.
        
        Returns:
            list: Lista de claves (valores) del nodo.
        """
        return self._claves

    @property
    def hijos(self):
        """
        Obtiene la lista de referencias a nodos hijos.
        
        Returns:
            list: Lista de referencias a nodos hijos (puede contener None).
        """
        return self._hijos

    def es_hoja(self):
        """
        Determina si el nodo es una hoja (no tiene hijos).
        
        Returns:
            bool: True si el nodo es una hoja, False en caso contrario.
        """
        return all(hijo is None for hijo in self.hijos)

    def esta_lleno(self):
        """
        Determina si el nodo está lleno (alcanzó la capacidad máxima de claves).
        
        Un nodo está lleno cuando contiene orden - 1 claves.
        
        Returns:
            bool: True si el nodo está lleno, False en caso contrario.
        """
        return len(self.claves) >= self.orden - 1