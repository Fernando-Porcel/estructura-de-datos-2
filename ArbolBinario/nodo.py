class Nodo:
    """
    Representa un nodo individual en un árbol binario.
    """

    def __init__(self, valor: int) -> None:
        """
        Inicializa un nuevo nodo con un valor y sin hijos.

        Args:
            valor (int): El valor entero a almacenar en el nodo.
        """
        self._valor: int = valor
        self._izquierdo: Nodo | None = None
        self._derecho: Nodo | None = None

    @property
    def valor(self) -> int:
        """
        Obtiene el valor almacenado en el nodo.

        Returns:
            int: El valor entero del nodo.
        """
        return self._valor
    
    @valor.setter
    def valor(self, nuevo_valor: int) -> None:
        """
        Define el valor del nodo.

        Args:
            nuevo_valor (int): El nuevo valor entero a asignar al nodo.
        """
        self._valor = nuevo_valor

    @property
    def izquierdo(self) -> Nodo:
        """
        Obtiene el nodo hijo izquierdo.

        Returns:
            Nodo: El nodo hijo izquierdo o None si no tiene.
        """
        return self._izquierdo
    
    @izquierdo.setter
    def izquierdo(self, nodo: Nodo) -> None:
        """
        Define el nodo hijo izquierdo.

        Args:
            nodo (Nodo): El nodo a establecer como hijo izquierdo.
        """
        self._izquierdo = nodo

    @property
    def derecho(self) -> Nodo:
        """
        Obtiene el nodo hijo derecho.

        Returns:
            Nodo: El nodo hijo derecho o None si no tiene.
        """
        return self._derecho
    
    @derecho.setter
    def derecho(self, nodo: Nodo) -> None:
        """
        Define el nodo hijo derecho.

        Args:
            nodo (Nodo): El nodo a establecer como hijo derecho.
        """
        self._derecho = nodo

    def es_hoja(self) -> bool:
        """
        Indica si el nodo no tiene hijos (es una hoja).

        Returns:
            bool: True si el nodo no tiene hijos, False en caso contrario.
        """
        return self.izquierdo is None and self.derecho is None