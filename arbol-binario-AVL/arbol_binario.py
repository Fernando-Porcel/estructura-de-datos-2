from nodo import Nodo
from collections import deque


class ArbolBinario:
    """
    Clase que gestiona la estructura de un árbol binario.
    """

    def __init__(self) -> None:
        """Inicializa un árbol vacío."""
        self._raiz: Nodo = None
        self._tamanio: int = 0

    @property
    def raiz(self) -> Nodo:
        """Obtiene el nodo raíz del árbol."""
        return self._raiz
    
    @raiz.setter
    def raiz(self, nodo_raiz: Nodo) -> None:
        """Establece el nodo raíz del árbol."""
        self._raiz = nodo_raiz

    def cantidad(self) -> int:
        """Retorna el número total de nodos en el árbol."""
        return self._tamanio

    def es_vacio(self) -> bool:
        """Verifica si el arbol binario esta vacio"""
        return self.raiz is None
    
    def altura(self) -> int:
        """Retorna la altura máxima del árbol."""
        return self._obtener_altura(self.raiz)
    
    def buscar_iterativo(self, valor: int) -> bool:
        """Busca un valor en el árbol y retorna True si existe."""
        nodo = self.raiz

        while nodo:
            if nodo.valor == valor:
                return True
            nodo = nodo.izquierdo if valor < nodo.izquierdo else nodo.derecho

        return False

    def buscar(self, valor: int) -> bool:
        """Busca un valor en el árbol y retorna True si existe."""
        return self._buscar_recursivo(valor, self.raiz)

    def _buscar_recursivo(self, valor: int, nodo: Nodo) -> bool:
        """Auxiliar recursivo para buscar."""
        if nodo is None:
            return False
        
        if valor == nodo.valor:
            return True

        if valor < nodo.valor:
            return self._buscar_recursivo(valor, nodo.izquierdo)
        return self._buscar_recursivo(valor, nodo.derecho)

    def amplitud(self) -> int:
        """Calcula el ancho máximo (máximo de nodos por nivel)."""
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

    def in_orden(self) -> list:
        """Recorrido en-orden: izq → raíz → der. Produce lista ordenada."""
        resultado = []
        self._in_orden(self.raiz, resultado)
        return resultado
    
    def _in_orden(self, nodo: Nodo, resultado: list) -> None:
        if nodo:
            self._in_orden(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._in_orden(nodo.derecho, resultado)

    def pre_orden(self) -> list:
        """Recorrido pre-orden: raíz → izq → der."""
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado
    
    def _pre_orden(self, nodo: Nodo, resultado: list) -> None:
        if nodo:
            resultado.append(nodo.valor)
            self._pre_orden(nodo.izquierdo, resultado)
            self._pre_orden(nodo.derecho, resultado)

    def post_orden(self) -> list:
        """Recorrido post-orden: izq → der → raíz."""
        resultado = []
        self._post_orden(self.raiz, resultado)
        return resultado
    
    def _post_orden(self, nodo: Nodo, resultado: list) -> None:
        if nodo:
            self._post_orden(nodo.izquierdo, resultado)
            self._post_orden(nodo.derecho, resultado)
            resultado.append(nodo.valor)

    def _obtener_altura(self, nodo: Nodo) -> int:
        """Retorna la altura del nodo dado, o 0 si es None."""
        return nodo._altura if nodo is not None else 0
    
    def _factor_equilibrio(self, nodo: Nodo) -> int:
        """Calcula el factor de equilibrio del nodo"""
        altura_izq = self._obtener_altura(nodo.izquierdo)
        altura_der = self._obtener_altura(nodo.derecho)

        return altura_izq - altura_der

    def _rotar_derecha(self, nodo: Nodo) -> Nodo:
        """Realiza una rotación simple a la derecha para balancear el árbol."""
        nuevo_padre = nodo.izquierdo
        subarbol_derecho = nuevo_padre.derecho

        nuevo_padre.derecho = nodo
        nodo.izquierdo = subarbol_derecho

        nodo._altura = 1 + max(
            self._obtener_altura(nodo._izquierdo),
            self._obtener_altura(nodo._derecho)
        )

        nuevo_padre._altura = 1 + max(
            self._obtener_altura(nuevo_padre._izquierdo),
            self._obtener_altura(nuevo_padre._derecho)
        )

        return nuevo_padre

    def _rotar_izquierda(self, nodo: Nodo) -> Nodo:
        """Realiza una rotación simple a la izquierda para balancear el árbol."""
        nuevo_padre = nodo.derecho
        subarbol_izquierdo = nuevo_padre.izquierdo

        nuevo_padre.izquierdo = nodo
        nodo.derecho = subarbol_izquierdo

        nodo._altura = 1 + max(
            self._obtener_altura(nodo._izquierdo),
            self._obtener_altura(nodo._derecho)
        )

        nuevo_padre._altura = 1 + max(
            self._obtener_altura(nuevo_padre._izquierdo),
            self._obtener_altura(nuevo_padre._derecho)
        )

        return nuevo_padre

    def insertar(self, valor: int) -> None:
        """Inserta un nuevo valor en el árbol de forma ordenada."""
        self.raiz = self._insertar_recursivo(valor, self.raiz)

    def _insertar_recursivo(self, valor: int, nodo: Nodo) -> Nodo:
        """Método privado para la inserción lógica recursiva."""
        if nodo is None:
            self._tamanio += 1
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(valor, nodo.izquierdo)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(valor, nodo.derecho)
        else:
            return nodo
        
        nodo._altura = 1 + max(
            self._obtener_altura(nodo.izquierdo), 
            self._obtener_altura(nodo.derecho)
        )

        balance = self._factor_equilibrio(nodo)

        if balance > 1 and valor < nodo.izquierdo.valor:
            return self._rotar_derecha(nodo)

        if balance < -1 and valor > nodo.derecho.valor:
            return self._rotar_izquierda(nodo)

        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)

        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        
        return nodo
    
    def _minimo_nodo(self, nodo: Nodo) -> Nodo:
        """Encuentra el nodo con el valor mínimo en el subárbol dado."""
        actual = nodo

        while actual.izquierdo is not None:
            actual = actual.izquierdo

        return actual

    def eliminar(self, valor: int) -> None:
        self.raiz, eliminado = self._eliminar_recur(valor, self.raiz)

        if eliminado:
            self._tamanio -= 1

    def _eliminar_recur(self, valor: int, nodo: Nodo) -> tuple[Nodo, bool]:
        """Método recursivo auxiliar para eliminar un valor del árbol y 
        rebalancearlo."""
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
            nodo.derecho, sw=self._eliminar_recur(sucesor.valor, nodo.derecho)
        
        if not sw:
            return nodo, False

        nodo._altura = 1 + max(
            self._obtener_altura(nodo.izquierdo), 
            self._obtener_altura(nodo.derecho)
        )

        balance = self._factor_equilibrio(nodo)

        if balance > 1 and self._factor_equilibrio(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo), True

        if balance < -1 and self._factor_equilibrio(nodo.izquierdo) < 0:
            return self._rotar_izquierda(nodo), True

        if balance > 1 and self._factor_equilibrio(nodo.derecho) <= 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo), True

        if balance < -1 and self._factor_equilibrio(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo), True

        return nodo, True

    def imprimir(self) -> None:
        """Muestra el árbol en consola con una rotación de 90°."""
        self._imprimir_rec(self.raiz, 0)
    
    def _imprimir_rec(self, nodo: Nodo, nivel: int) -> None:
        """Método auxiliar recursivo para imprimir el árbol de manera visual."""
        if nodo:
            self._imprimir_rec(nodo.derecho, nivel + 1)
            print("    " * nivel + f"[{nodo.valor}]")
            self._imprimir_rec(nodo.izquierdo, nivel + 1)
