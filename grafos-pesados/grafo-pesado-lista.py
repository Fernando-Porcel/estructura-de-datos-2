from collections import deque, heapq

class GrafoPesadoLista:
    """Implementación de un grafo pesado (ponderado) basado en lista de adyacencia.
    
    Utiliza un diccionario para almacenar vértices y sus adyacencias con pesos.
    Cada arista se representa como una tupla (destino, peso).
    Permite operaciones como búsquedas BFS/DFS, cálculo de caminos más cortos
    usando el algoritmo de Dijkstra, y detección de ciclos.
    
    Atributos:
        _lista (dict): Diccionario que almacena vértices y sus vecinos con pesos.
        _dirigido (bool): Indica si el grafo es dirigido o no.
    """
    def __init__(self, dirigido):
        """Inicializa un nuevo grafo pesado vacío.
        
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

    def agregar_arista(self, origen, destino, peso):
        """Agrega una arista ponderada entre dos vértices.
        
        Si los vértices no existen, los crea automáticamente.
        Para grafos no dirigidos, agrega la arista en ambas direcciones con el mismo peso.
        
        Args:
            origen: Vértice de origen.
            destino: Vértice de destino.
            peso (float): Peso de la arista.
        """
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)

        if destino not in [v for v, _ in self._lista[origen]]:
            self._lista[origen].append((destino, peso))

        if not self.dirigido and origen not in [v for v, _ in self._lista[destino]]:
            self._lista[destino].append((origen, peso))
        
    def eliminar_arista(self, origen, destino):
        """Elimina una arista entre dos vértices.
        
        Para grafos no dirigidos, elimina la arista en ambas direcciones.
        
        Args:
            origen: Vértice de origen.
            destino: Vértice de destino.
        """
        if origen in self._lista:
            self._lista[origen] = [(v, p) for v, p in self._lista[origen] if v != destino]

        if not self.dirigido and destino in self._lista:
            self._lista[destino] = [(v, p) for v, p in self._lista[destino] if v != origen]

    def vecinos(self, vertice):
        """Retorna la lista de vecinos con sus pesos (vértices adyacentes).
        
        Args:
            vertice: Identificador del vértice.
            
        Returns:
            list: Lista de tuplas (vecino, peso) adyacentes al vértice dado.
        """
        return self._lista.get(vertice, [])

    def mostrar_lista(self):
        """Imprime la lista de adyacencia del grafo pesado.
        
        Muestra cada vértice y sus vecinos con sus respectivos pesos.
        Formato: vértice -> [(vecino1, peso1), (vecino2, peso2), ...]
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

        for vecino, _ in self.vecinos(vertice):
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

            for vecino, _ in self.vecinos(vertice):
                if vecino not in visitados:
                    cola.append(vecino)
                    visitados.add(vecino)

        return resultado
    
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

        for vecino, _ in self.vecinos(vertice):
            if vecino not in visitados:
                if self._dfs_ciclo(vecino, visitados, padre=vertice):
                    return True
            elif vecino != padre:
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

        for vecino, _ in self.vecinos(vertice):
            if vecino not in visitados:
                self._dfs_topo(vecino, visitados, resultado)

        resultado.append(vertice)

    def dijkstra(self, origen, destino):
        """Encuentra el camino más corto entre dos vértices usando el algoritmo de Dijkstra.
        
        Utiliza el algoritmo de Dijkstra que es óptimo para grafos con pesos positivos.
        
        Args:
            origen: Vértice de inicio.
            destino: Vértice de destino.
            
        Returns:
            tuple: (camino, distancia) donde camino es la lista de vértices
                   y distancia es el peso total del camino.
            None: Si no existe camino entre los vértices.
        """
        if origen not in self._lista or destino not in self._lista:
            return None

        # Inicializa distancias y predecesores
        distancias = {v: float('inf') for v in self._lista}
        distancias[origen] = 0
        predecesores = {v: None for v in self._lista}
        heap = [(0, origen)]  # (distancia, vértice)

        # Procesa vértices en orden de distancia (heap)
        while heap:
            dist_actual, actual = heapq.heappop(heap)

            # Relaja aristas del vértice actual
            for vecino, peso in self.vecinos(actual):
                nueva_dist = dist_actual + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    predecesores[vecino] = actual
                    heapq.heappush(heap, (nueva_dist, vecino))

        if distancias[destino] == float('inf'):
            return None

        return self._reconstruir_camino(predecesores, destino), distancias[destino]

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

        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]
        
        return camino[::-1]