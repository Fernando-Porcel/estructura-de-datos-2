from collections import deque

class GrafoLista:
    """Implementación de un grafo basado en lista de adyacencia.
    
    Utiliza un diccionario para almacenar los vértices y sus adyacencias.
    Permite operaciones como agregar/eliminar aristas, búsquedas BFS/DFS,
    encontrar caminos más cortos y detectar ciclos.
    
    Atributos:
        _lista (dict): Diccionario que almacena vértices y sus vecinos.
        _dirigido (bool): Indica si el grafo es dirigido o no.
    """
    def __init__(self, dirigido):
        """Inicializa un nuevo grafo vacío.
        
        Args:
            dirigido (bool): Si True, crea un grafo dirigido; si False, no dirigido.
        """
        self._lista = {}
        self._dirigido = dirigido

    @property
    def dirigido(self):
        """Retorna si el grafo es dirigido.
        
        Returns:
            bool: True si el grafo es dirigido, False si no.
        """
        return self._dirigido
    
    def agregar_vertice(self, origen):
        """Agrega un nuevo vértice al grafo.
        
        Si el vértice ya existe, no realiza ninguna acción.
        
        Args:
            origen: Identificador del vértice a agregar.
        """
        if origen not in self._lista:
            self._lista[origen] = []

    def agregar_arista(self, origen, destino):
        """Agrega una arista entre dos vértices.
        
        Si los vértices no existen, los crea automáticamente.
        Para grafos no dirigidos, agrega la arista en ambas direcciones.
        
        Args:
            origen: Vértice de origen.
            destino: Vértice de destino.
        """
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)

        if destino not in self._lista[origen]:
            self._lista[origen].append(destino)

        # Si no es dirigido, agrega la arista inversa
        if not self.dirigido and origen not in self._lista[destino]:
            self._lista[destino].append(origen)

    def eliminar_arista(self, origen, destino):
        """Elimina una arista entre dos vértices.
        
        Para grafos no dirigidos, elimina la arista en ambas direcciones.
        
        Args:
            origen: Vértice de origen.
            destino: Vértice de destino.
        """
        if origen in self._lista and destino in self._lista[origen]:
            self._lista[origen].remove(destino)
        
        # Si no es dirigido, elimina la arista inversa
        if not self.dirigido:
            if destino in self._lista and origen in self._lista[destino]:
                self._lista[destino].remove(origen)

    def vecinos(self, vertice):
        """Retorna la lista de vecinos (vértices adyacentes) de un vértice.
        
        Args:
            vertice: Identificador del vértice.
            
        Returns:
            list: Lista de vértices adyacentes al vértice dado.
        """
        return self._lista.get(vertice, [])

    def mostrar_lista(self):
        """Imprime la lista de adyacencia del grafo.
        
        Muestra cada vértice y sus vecinos en el formato: vértice -> [vecinos]
        """
        for vertice, vecinos in self._lista.items():
            print(f"{vertice} -> {vecinos}")

    def dfs(self, vertice):
        """Realiza una búsqueda en profundidad (DFS) desde un vértice.
        
        Args:
            vertice: Vértice inicial de la búsqueda.
            
        Returns:
            list: Lista de vértices visitados en orden DFS.
        """
        if vertice not in self._lista:
            return []
        
        resultado = []
        visitados = set()
        self._dfs_rec(vertice, visitados, resultado)
        return resultado
    
    def _dfs_rec(self, vertice, visitados, resultado):
        """Auxiliar recursivo para DFS.
        
        Args:
            vertice: Vértice actual a procesar.
            visitados: Conjunto de vértices ya visitados.
            resultado: Lista donde se acumulan los vértices visitados.
        """
        visitados.add(vertice)
        resultado.append(vertice)

        # Recorre recursivamente cada vecino no visitado
        for vecino in self.vecinos(vertice):
            if vecino not in visitados:
                self._dfs_rec(vecino, visitados, resultado)

    def bfs(self, inicio):
        """Realiza una búsqueda en anchura (BFS) desde un vértice.
        
        Args:
            inicio: Vértice inicial de la búsqueda.
            
        Returns:
            list: Lista de vértices visitados en orden BFS.
        """
        if inicio not in self._lista:
            return []

        visitados = set()
        cola = deque([inicio])
        resultado = []
        visitados.add(inicio)

        while cola:
            vertice = cola.popleft()
            resultado.append(vertice)

            for vecino in self.vecinos(vertice):
                if vecino not in visitados:
                    cola.append(vecino)
                    visitados.add(vecino)

        return resultado
    
    def camino_mas_corto(self, origen, destino):
        """Encuentra el camino más corto entre dos vértices usando BFS.
        
        Args:
            origen: Vértice de inicio.
            destino: Vértice de destino.
            
        Returns:
            list: Lista de vértices que forman el camino más corto.
            None: Si no existe camino entre los vértices.
        """
        if origen not in self._lista or destino not in self._lista:
            return None
        
        if origen == destino:
            return [origen]
        
        visitados = {origen: None}
        cola = deque([origen])

        while cola:
            actual = cola.popleft()

            for vecino in self.vecinos(actual):
                if vecino not in visitados:
                    visitados[vecino] = actual
                    if vecino == destino:
                        return self._reconstruir_camino(visitados, destino)
                    cola.append(vecino)

        return None

    def _reconstruir_camino(self, predecesores, destino):
        """Reconstruye el camino desde el diccionario de predecesores.
        
        Args:
            predecesores: Diccionario que mapea cada vértice a su predecesor.
            destino: Vértice final del camino.
            
        Returns:
            list: Camino reconstructo del origen al destino.
        """
        camino = []
        actual = destino

        # Recorre hacia atrás desde el destino hasta el origen
        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]

        return camino[::-1]  # Invierte para obtener orden origen -> destino

    def tiene_ciclo(self):
        """Detecta si el grafo contiene ciclos.
        
        Returns:
            bool: True si el grafo tiene ciclos, False en caso contrario.
        """
        visitados = set()
        for vertice in self._lista:
            if vertice not in visitados:
                if self._dfs_ciclo(vertice, visitados, padre=-1):
                    return True
                
        return False

    def _dfs_ciclo(self, vertice, visitados, padre):
        """Auxiliar DFS para detectar ciclos.
        
        Un ciclo se detecta cuando se encuentra una arista hacia un vértice
        ya visitado que no es el padre del vértice actual.
        
        Args:
            vertice: Vértice actual.
            visitados: Conjunto de vértices visitados.
            padre: Vértice padre en el árbol de recorrido.
            
        Returns:
            bool: True si se detecta un ciclo, False en caso contrario.
        """
        visitados.add(vertice)

        for vecino in self.vecinos(vertice):
            if vecino not in visitados:
                if self._dfs_ciclo(vecino, visitados, padre=vertice):
                    return True
            elif vecino != padre:  # Encontró un vértice visitado que no es el padre
                return True
                
        return False
    
    def orden_topologico(self):
        """Calcula el orden topológico del grafo dirigido acíclico (DAG).
        
        Solo es válido para grafos dirigidos sin ciclos.
        
        Returns:
            list: Lista de vértices en orden topológico.
            None: Si el grafo es no dirigido o contiene ciclos.
        """
        if self.tiene_ciclo() or not self.dirigido:
            return None
        
        visitados = set()
        resultado = []

        for vertice in self._lista:
            if vertice not in visitados:
                self._dfs_topo(vertice, visitados, resultado)

        return resultado[::-1]

    def _dfs_topo(self, vertice, visitados, resultado):
        """Auxiliar DFS para calcular orden topológico.
        
        Los vértices se añaden al resultado después de procesar todos
        sus descendientes (postorden).
        
        Args:
            vertice: Vértice actual.
            visitados: Conjunto de vértices visitados.
            resultado: Lista donde se acumulan los vértices en postorden.
        """
        visitados.add(vertice)

        for vecino in self.vecinos(vertice):
            if vecino not in visitados:
                self._dfs_topo(vecino, visitados, resultado)

        resultado.append(vertice)