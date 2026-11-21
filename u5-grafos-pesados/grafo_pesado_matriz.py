from collections import deque
import heapq

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
        """
        Detecta si el grafo (dirigido) tiene ciclos usando DFS.
        Usa coloreado de nodos: blanco=no visitado, gris=en proceso, negro=terminado.
        """
        COLOR_BLANCO, COLOR_GRIS, COLOR_NEGRO = 0, 1, 2
        color = {v: COLOR_BLANCO for v in range(self.num_vertices)}
        
        def dfs_ciclo(v) -> bool:
            color[v] = COLOR_GRIS
            for vecino in range(self.num_vertices):
                if self._matriz[v][vecino] != 0:
                    if color[vecino] == COLOR_GRIS:
                        return True  # arista al gris = ciclo
                    if color[vecino] == COLOR_BLANCO and dfs_ciclo(vecino):
                        return True
            color[v] = COLOR_NEGRO
            return False
        
        for v in range(self.num_vertices):
            if color[v] == COLOR_BLANCO:
                if dfs_ciclo(v):
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

    # ------------------------------------------------------------------
    # Bellman-Ford (camino más corto, admite pesos negativos)
    # ------------------------------------------------------------------
    def bellman_ford(self, origen, destino):
        """Camino más corto entre dos vértices con el algoritmo de Bellman-Ford.

        A diferencia de Dijkstra, admite aristas con peso negativo. Relaja
        todas las aristas V-1 veces; si todavía se puede mejorar una distancia
        después de eso, existe un ciclo de peso negativo.

        Args:
            origen (int): Índice del vértice de inicio.
            destino (int): Índice del vértice de destino.

        Returns:
            tuple: (camino, distancia).
            None: Si algún vértice no existe o no hay camino.

        Raises:
            ValueError: Si hay un ciclo negativo alcanzable desde el origen.
        """
        if (origen < 0 or origen >= self.num_vertices
                or destino < 0 or destino >= self.num_vertices):
            return None

        distancias = {v: float('inf') for v in range(self.num_vertices)}
        distancias[origen] = 0
        predecesores = {v: None for v in range(self.num_vertices)}

        # V-1 rondas: en cada una se relajan TODAS las aristas
        for _ in range(self.num_vertices - 1):
            hubo_cambio = False
            for u in range(self.num_vertices):
                if distancias[u] == float('inf'):
                    continue  # todavía no se llega a u
                for v in range(self.num_vertices):
                    peso = self._matriz[u][v]
                    if peso != 0 and distancias[u] + peso < distancias[v]:
                        distancias[v] = distancias[u] + peso
                        predecesores[v] = u
                        hubo_cambio = True
            if not hubo_cambio:
                break  # ya está estable, no hace falta seguir

        # Ronda extra: si aún mejora algo, hay ciclo negativo
        for u in range(self.num_vertices):
            if distancias[u] == float('inf'):
                continue
            for v in range(self.num_vertices):
                peso = self._matriz[u][v]
                if peso != 0 and distancias[u] + peso < distancias[v]:
                    raise ValueError("El grafo tiene un ciclo de peso negativo")

        if distancias[destino] == float('inf'):
            return None

        return self._reconstruir_camino(predecesores, destino), distancias[destino]

    # ------------------------------------------------------------------
    # Árbol de expansión de costo mínimo (solo grafos NO dirigidos)
    # ------------------------------------------------------------------
    def kruskal(self):
        """Árbol de expansión de costo mínimo con el algoritmo de Kruskal.

        Ordena las aristas por peso y agrega la más barata que no forme ciclo
        (usa Union-Find para detectar ciclos).

        Returns:
            tuple: (aristas, costo_total) con aristas como lista de (u, v, peso).
            None: Si el grafo es dirigido o no es conexo.
        """
        if self.dirigido:
            return None
        if self.num_vertices == 0:
            return [], 0

        # Solo la mitad superior de la matriz: cada arista una sola vez
        aristas = []
        for u in range(self.num_vertices):
            for v in range(u + 1, self.num_vertices):
                if self._matriz[u][v] != 0:
                    aristas.append((self._matriz[u][v], u, v))
        aristas.sort(key=lambda a: a[0])

        # Union-Find: cada vértice empieza en su propio grupo
        padre = list(range(self.num_vertices))

        def buscar(x):
            while padre[x] != x:
                padre[x] = padre[padre[x]]  # compresión de caminos
                x = padre[x]
            return x

        mst = []
        costo_total = 0
        for peso, u, v in aristas:
            raiz_u, raiz_v = buscar(u), buscar(v)
            if raiz_u != raiz_v:            # distintos grupos: no forma ciclo
                padre[raiz_u] = raiz_v      # los une
                mst.append((u, v, peso))
                costo_total += peso

        if len(mst) != self.num_vertices - 1:
            return None  # no conexo
        return mst, costo_total

    def prim(self, inicio=0):
        """Árbol de expansión de costo mínimo con el algoritmo de Prim.

        Parte de un vértice y en cada paso toma la arista más barata que
        conecta lo ya visitado con un vértice nuevo (usa un heap).

        Args:
            inicio (int): Vértice inicial (por defecto 0).

        Returns:
            tuple: (aristas, costo_total) con aristas como lista de (u, v, peso).
            None: Si el grafo es dirigido o no es conexo.
        """
        if self.dirigido:
            return None
        if self.num_vertices == 0:
            return [], 0
        if inicio < 0 or inicio >= self.num_vertices:
            return None

        visitados = {inicio}
        heap = [(self._matriz[inicio][v], inicio, v)
                for v in range(self.num_vertices) if self._matriz[inicio][v] != 0]
        heapq.heapify(heap)
        mst = []
        costo_total = 0

        while heap and len(visitados) < self.num_vertices:
            peso, u, v = heapq.heappop(heap)
            if v in visitados:
                continue  # esa arista ya no aporta
            visitados.add(v)
            mst.append((u, v, peso))
            costo_total += peso
            for w in range(self.num_vertices):
                if self._matriz[v][w] != 0 and w not in visitados:
                    heapq.heappush(heap, (self._matriz[v][w], v, w))

        if len(visitados) != self.num_vertices:
            return None  # no conexo
        return mst, costo_total