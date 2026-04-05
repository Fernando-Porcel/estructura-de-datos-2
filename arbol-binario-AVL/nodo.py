class Nodo:
    """
    Representa un nodo individual en un árbol binario.
    """

    def __init__(self, valor: int) -> None:
        """
        Inicializa un nuevo nodo con un valor y sin hijos.
        """
        self._valor: int = valor
        self._izquierdo: Nodo = None
        self._derecho: Nodo = None
        self._altura: int = 1

    @property
    def valor(self) -> int:
        """Obtiene el valor almacenado en el nodo."""
        return self._valor
    
    @valor.setter
    def valor(self, nuevo_valor: int) -> None:
        """Define el valor del nodo."""
        self._valor = nuevo_valor

    @property
    def izquierdo(self) -> Nodo:
        """Obtiene el nodo hijo izquierdo."""
        return self._izquierdo
    
    @izquierdo.setter
    def izquierdo(self, nodo: Nodo) -> None:
        """Define el nodo hijo izquierdo."""
        self._izquierdo = nodo

    @property
    def derecho(self) -> Nodo:
        """Obtiene el nodo hijo derecho."""
        return self._derecho
    
    @derecho.setter
    def derecho(self, nodo: Nodo) -> None:
        """Define el nodo hijo derecho."""
        self._derecho = nodo

    def es_hoja(self) -> bool:
        """Indica si el nodo no tiene hijos (es una hoja)."""
        return self.izquierdo is None and self.derecho is None