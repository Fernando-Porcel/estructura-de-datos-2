from collections import deque, heapq

class GrafoPesadoMatriz:
    """Implementación de un grafo pesado (ponderado) basado en matriz de adyacencia.
    
    Utiliza una matriz cuadrada para almacenar los pesos de las aristas.
    El valor 0 en la matriz indica ausencia de arista, valores distintos de 0
    representan el peso de la arista.
    Permite operaciones como búsquedas BFS/DFS, cálculo de caminos más cortos
    usando el algoritmo de Dijkstra, y detección de ciclos.
    
    Atributos:
        _num_vertices (int): Número total de vértices del grafo.
        _matriz (list[list]): Matriz de adyacencia (num_vertices x num_vertices).
        _dirigido (bool): Indica si el grafo es dirigido o no.
    """
    def __init__(self, num_vertices, dirigido=False):
        """Inicializa un nuevo grafo pesado con matriz de adyacencia.
        
        Args:
            num_vertices (int): Número de vértices del grafo (0 a num_vertices-1).
            dirigido (bool): Si True, crea un grafo dirigido; si False, no dirigido.
                            Por defecto es False.
        """
        self._num_vertices = num_vertices
        # Crea una matriz inicializada con ceros (sin aristas)
        self._matriz = [[0] * num_vertices for _ in range(num_vertices)]
        self._dirigido = dirigido

    @property
    def num_vertices(self):
        """Retorna el número de vértices del grafo.
        
        Returns:
            int: Número de vértices.
        """
        return self._num_vertices
    
    @property
    def dirigido(self):
        """Retorna si el grafo es dirigido.
        
        Returns:
            bool: True si el grafo es dirigido, False si no.
        """
        return self._dirigido
    
    def agregar_arista(self, origen, destino, peso):
        """Agrega una arista ponderada entre dos vértices.
        
        Para grafos no dirigidos, agrega la arista en ambas direcciones con el mismo peso.
        
        Args:
            origen (int): Índice del vértice de origen (0 <= origen < num_vertices).
            destino (int): Índice del vértice de destino (0 <= destino < num_vertices).
            peso (float): Peso de la arista (debe ser distinto de 0).
        """
        self._matriz[origen][destino] = peso

        if not self.dirigido:
            self._matriz[destino][origen] = peso

    def eliminar_arista(self, origen, destino):
        """Elimina una arista entre dos vértices.
        
        Para grafos no dirigidos, elimina la arista en ambas direcciones.
        
        Args:
            origen (int): Índice del vértice de origen.
            destino (int): Índice del vértice de destino.
        """
        self._matriz[origen][destino] = 0

        if not self.dirigido:
            self._matriz[destino][origen] = 0
    
    def mostrar_matriz(self):
        """Imprime la matriz de adyacencia del grafo pesado.
        
        Muestra cada fila de la matriz de adyacencia con los pesos.
        """
        for i in range(self.num_vertices):
            print(self._matriz[i])

    def dfs(self, vertice):
        """Realiza una búsqueda en profundidad (DFS) desde un vértice.
        
        Args:
            vertice (int): Índice del vértice inicial de la búsqueda.
            
        Returns:
            list: Lista de vértices visitados en orden DFS.
        """
        if vertice < 0 or vertice >= self.num_vertices:
            return []
        
        resultado = []
        visitados = set()
        self._dfs_rec(vertice, visitados, resultado)
        return resultado
    
    def _dfs_rec(self, vertice, visitados, resultado):
        """Auxiliar recursivo para DFS.
        
        Args:
            vertice (int): Vértice actual a procesar.
            visitados (set): Conjunto de vértices ya visitados.
            resultado (list): Lista donde se acumulan los vértices visitados.
        """
        visitados.add(vertice)
        resultado.append(vertice)

        for vecino in range(self.num_vertices):
            if self._matriz[vertice][vecino] != 0 and vecino not in visitados:
                self._dfs_rec(vecino, visitados, resultado)

    def bfs(self, inicio):
        """Realiza una búsqueda en anchura (BFS) desde un vértice.
        
        Args:
            inicio (int): Índice del vértice inicial de la búsqueda.
            
        Returns:
            list: Lista de vértices visitados en orden BFS.
        """
        if inicio < 0 or inicio >= self.num_vertices:
            return []

        visitados = set()
        cola = deque([inicio])
        resultado = []
        visitados.add(inicio)
        
        while cola:
            vertice = cola.popleft()
            resultado.append(vertice)

            for vecino in range(self.num_vertices):
                if self._matriz[vertice][vecino] != 0 and vecino not in visitados:
                    cola.append(vecino)
                    visitados.add(vecino)

        return resultado
    
    def tiene_ciclo(self):
        """Detecta si el grafo contiene ciclos.
        
        Returns:
            bool: True si el grafo tiene ciclos, False en caso contrario.
        """
        visitados = set()
        for vertice in range(self.num_vertices):
            if vertice not in visitados:
                if self._dfs_ciclo(vertice, visitados, padre=-1):
                    return True
                
        return False

    def _dfs_ciclo(self, vertice, visitados, padre):
        """Auxiliar DFS para detectar ciclos.
        
        Un ciclo se detecta cuando se encuentra una arista hacia un vértice
        ya visitado que no es el padre del vértice actual.
        
        Args:
            vertice (int): Vértice actual.
            visitados (set): Conjunto de vértices visitados.
            padre (int): Vértice padre en el árbol de recorrido.
            
        Returns:
            bool: True si se detecta un ciclo, False en caso contrario.
        """
        visitados.add(vertice)

        for vecino in range(self.num_vertices):
            if self._matriz[vertice][vecino] != 0:
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

        for vertice in range(self.num_vertices):
            if vertice not in visitados:
                self._dfs_topo(vertice, visitados, resultado)

        return resultado[::-1]  # Invierte el orden del DFS para obtener orden topológico

    def _dfs_topo(self, vertice, visitados, resultado):
        """Auxiliar DFS para calcular orden topológico.
        
        Los vértices se añaden al resultado después de procesar todos
        sus descendientes (postorden).
        
        Args:
            vertice (int): Vértice actual.
            visitados (set): Conjunto de vértices visitados.
            resultado (list): Lista donde se acumulan los vértices en postorden.
        """
        visitados.add(vertice)

        for vecino in range(self.num_vertices):
            if self._matriz[vertice][vecino] != 0 and vecino not in visitados:
                self._dfs_topo(vecino, visitados, resultado)

        resultado.append(vertice)

    def dijkstra(self, origen, destino):
        """Encuentra el camino más corto entre dos vértices usando el algoritmo de Dijkstra.
        
        Utiliza el algoritmo de Dijkstra que es óptimo para grafos con pesos positivos.
        
        Args:
            origen (int): Índice del vértice de inicio.
            destino (int): Índice del vértice de destino.
            
        Returns:
            tuple: (camino, distancia) donde camino es la lista de vértices
                   y distancia es el peso total del camino.
            None: Si no existe camino entre los vértices.
        """
        if origen < 0 or destino < 0 or destino >= self.num_vertices:
            return None

        distancias = {v: float('inf') for v in range(self.num_vertices)}
        distancias[origen] = 0
        predecesores = {v: None for v in range(self.num_vertices)}
        heap = [(0, origen)]  # (distancia, vértice)

        # Procesa vértices en orden de distancia (heap)
        while heap:
            dist_actual, actual = heapq.heappop(heap)

            # Relaja aristas del vértice actual
            for vecino in range(self.num_vertices):
                if self._matriz[actual][vecino] != 0:  # Existe arista
                    nueva_dist = dist_actual + self._matriz[actual][vecino]
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
            predecesores (dict): Diccionario que mapea cada vértice a su predecesor.
            destino (int): Vértice final del camino.
            
        Returns:
            list: Camino reconstructo del origen al destino.
        """
        camino = []
        actual = destino

        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]
        
        return camino[::-1]