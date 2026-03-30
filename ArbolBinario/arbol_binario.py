from nodo import Nodo
from collections import deque


class ArbolBinario:
    """
    Clase que gestiona la estructura de un árbol binario.
    """

    def __init__(self) -> None:
        """
        Inicializa un árbol binario vacío.

        Attributes:
            _raiz (Nodo): El nodo raíz del árbol. Es None si el árbol está vacío.
            _tamanio (int): El número total de nodos en el árbol.
        """
        self._raiz: Nodo = None
        self._tamanio: int = 0

    @property
    def raiz(self) -> Nodo:
        """
        Obtiene el nodo raíz del árbol.

        Returns:
            Nodo: El nodo raíz del árbol.
        """
        return self._raiz
    
    @raiz.setter
    def raiz(self, nodo_raiz: Nodo) -> None:
        """
        Establece el nodo raíz del árbol.

        Args:
            nodo_raiz (Nodo): El nodo a establecer como raíz del árbol.
        """
        self._raiz = nodo_raiz

    def es_vacio(self) -> bool:
        """
        Verifica si el árbol binario está vacío.

        Returns:
            bool: True si el árbol no tiene nodos, False en caso contrario.
        """
        return self.raiz is None

    def buscar_iterativo(self, valor: int) -> bool:
        """
        Busca un valor en el árbol de manera iterativa sin usar recursión.

        Args:
            valor (int): El valor entero a buscar.

        Returns:
            bool: True si el valor existe en el árbol, False en caso contrario.
        """
        nodo = self.raiz

        while nodo:
            if nodo.valor == valor:
                return True
            nodo = nodo.izquierdo if valor < nodo.valor else nodo.derecho

        return False

    def buscar(self, valor: int) -> bool:
        """
        Busca un valor en el árbol y retorna True si existe.

        Args:
            valor (int): El valor a buscar en el árbol.

        Returns:
            bool: True si el valor se encuentra en el árbol, False en caso contrario.
        """
        return self._buscar_recursivo(valor, self.raiz)

    def _buscar_recursivo(self, valor: int, nodo: Nodo) -> bool:
        """
        Auxiliar recursivo para buscar un valor en el subárbol.

        Args:
            valor (int): El valor a buscar.
            nodo (Nodo): El nodo actual en la recursión.

        Returns:
            bool: True si el valor se encuentra en el subárbol, False en caso contrario.
        """
        if nodo is None:
            return False
        
        if valor == nodo.valor:
            return True

        if valor < nodo.valor:
            return self._buscar_recursivo(valor, nodo.izquierdo)
        return self._buscar_recursivo(valor, nodo.derecho)

    def insertar_iterativo(self, valor: int) -> None:
        """
        Inserta un nuevo valor en el árbol de forma iterativa.

        Args:
            valor (int): El valor entero que se desea insertar.
        """
        if self.raiz is None:
            self.raiz = Nodo(valor)
            self._tamanio += 1
            return

        nodo = self.raiz

        while True:
            if valor < nodo.valor:
                if nodo.izquierdo is None:
                    nodo.izquierdo = Nodo(valor)
                    self._tamanio += 1
                    return
                nodo = nodo.izquierdo
            elif valor > nodo.valor:
                if nodo.derecho is None:
                    nodo.derecho = Nodo(valor)
                    self._tamanio += 1
                    return
                nodo = nodo.derecho
            else:
                return

    def insertar(self, valor: int) -> None:
        """
        Inserta un nuevo valor en el árbol de forma ordenada.
        Si el valor ya existe, no se inserta duplicado.

        Args:
            valor (int): El valor entero que se desea insertar en el árbol.
        """
        self.raiz = self._insertar_recursivo(valor, self.raiz)

    def _insertar_recursivo(self, valor: int, nodo: Nodo) -> Nodo:
        """
        Método privado y recursivo para la inserción lógica de un valor.

        Args:
            valor (int): El valor a insertar.
            nodo (Nodo): El nodo actual en la recursión.

        Returns:
            Nodo: El nodo actual después de la inserción o un nuevo nodo si se llega a una hoja.
        """
        if nodo is None:
            self._tamanio += 1
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(valor, nodo.izquierdo)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(valor, nodo.derecho)

        return nodo

    def altura(self) -> int:
        """
        Retorna la altura máxima del árbol.

        Returns:
            int: La altura del árbol. Retorna 0 si el árbol está vacío.
        """
        return self._altura_recursivo(self.raiz)

    def _altura_recursivo(self, nodo: Nodo) -> int:
        """
        Calcula la altura de un subárbol de forma recursiva.

        Args:
            nodo (Nodo): El nodo actual en la recursión.

        Returns:
            int: La altura del subárbol, contando desde el nodo actual.
        """
        if nodo is None:
            return 0
        
        return 1 + max(self._altura_recursivo(nodo.izquierdo),
                       self._altura_recursivo(nodo.derecho))
    
    def amplitud(self) -> int:
        """
        Calcula el ancho máximo del árbol (el número máximo de nodos en un nivel).

        Returns:
            int: La amplitud máxima del árbol. Retorna 0 si el árbol está vacío.
        """
        if self.raiz is None:
            return 0
        
        cola = deque([self.raiz])
        max_amplitud = 0
        
        while cola:
            longitud_nivel = len(cola)
            max_amplitud = max(max_amplitud, longitud_nivel)

            for _ in range(longitud_nivel):
                nodo_actual = cola.popleft()

                if nodo_actual.izquierdo:
                    cola.append(nodo_actual.izquierdo)

                if nodo_actual.derecho:
                    cola.append(nodo_actual.derecho)

        return max_amplitud

    def cantidad(self) -> int:
        """
        Retorna el número total de nodos en el árbol.

        Returns:
            int: El número de nodos en el árbol.
        """
        return self._tamanio

    def in_orden(self) -> list:
        """
        Realiza un recorrido en-orden (izquierdo -> raíz -> derecho).
        Este recorrido produce los elementos en orden ascendente.

        Returns:
            list: Una lista con los valores del árbol ordenados.
        """
        resultado = []
        self._in_orden(self.raiz, resultado)
        return resultado
    
    def _in_orden(self, nodo: Nodo, resultado: list) -> None:
        """Auxiliar recursivo para el recorrido en-orden."""
        if nodo:
            self._in_orden(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._in_orden(nodo.derecho, resultado)

    def pre_orden(self) -> list:
        """
        Realiza un recorrido pre-orden (raíz -> izquierdo -> derecho).

        Returns:
            list: Una lista con los valores según el orden de visita.
        """
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado
    
    def _pre_orden(self, nodo: Nodo, resultado: list) -> None:
        """Auxiliar recursivo para el recorrido pre-orden."""
        if nodo:
            resultado.append(nodo.valor)
            self._pre_orden(nodo.izquierdo, resultado)
            self._pre_orden(nodo.derecho, resultado)

    def post_orden(self) -> list:
        """
        Realiza un recorrido post-orden (izquierdo -> derecho -> raíz).

        Returns:
            list: Una lista con los valores según el orden de visita.
        """
        resultado = []
        self._post_orden(self.raiz, resultado)
        return resultado
    
    def _post_orden(self, nodo: Nodo, resultado: list) -> None:
        """Auxiliar recursivo para el recorrido post-orden."""
        if nodo:
            self._post_orden(nodo.izquierdo, resultado)
            self._post_orden(nodo.derecho, resultado)
            resultado.append(nodo.valor)

    def _minimo_nodo(self, nodo: Nodo) -> Nodo:
        """Busca el nodo con el valor más pequeño en un subárbol."""
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def eliminar(self, valor: int) -> None:
        """
        Elimina la primera instancia de un valor específico en el árbol.

        Args:
            valor (int): El valor que se desea eliminar.
        """
        self.raiz, eliminado = self._eliminar_recur(valor, self.raiz)

        if eliminado:
            self._tamanio -= 1

    def _eliminar_recur(self, valor: int, nodo: Nodo) -> tuple[Nodo, bool]:
        """
        Método privado recursivo para gestionar la eliminación de un nodo.

        Args:
            valor (int): Valor a buscar y eliminar.
            nodo (Nodo): Nodo actual en la exploración.

        Returns:
            tuple[Nodo, bool]: El nodo (actualizado o nuevo) y un booleano que indica si se eliminó.
        """
        if nodo is None:
            return None, False
        
        if valor < nodo.valor:
            nodo.izquierdo, sw = self._eliminar_recur(valor, nodo.izquierdo)
        elif valor > nodo.valor:
            nodo.derecho, sw = self._eliminar_recur(valor, nodo.derecho)
        else:
            if nodo.es_hoja():
                return None, True
            
            if nodo.izquierdo is None:
                return nodo.derecho, True
            
            if nodo.derecho is None:
                return nodo.izquierdo, True
            
            sucesor = self._minimo_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho, sw = self._eliminar_recur(sucesor.valor, nodo.derecho)
        
        return nodo, sw

    def imprimir(self) -> None:
        """Muestra el árbol en consola con una rotación de 90°."""
        self._imprimir_rec(self.raiz, 0)
    
    def _imprimir_rec(self, nodo: Nodo, nivel: int) -> None:
        """Auxiliar recursivo para la representación visual del árbol."""
        if nodo:
            self._imprimir_rec(nodo.derecho, nivel + 1)
            print("    " * nivel + f"[{nodo.valor}]")
            self._imprimir_rec(nodo.izquierdo, nivel + 1)