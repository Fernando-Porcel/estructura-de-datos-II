from collections import deque
import heapq

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
    def __init__(self, dirigido=False):
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
        """
        Detecta si el grafo (dirigido) tiene ciclos usando DFS.
        Usa coloreado de nodos: blanco=no visitado, gris=en proceso, negro=terminado.
        """
        COLOR_BLANCO, COLOR_GRIS, COLOR_NEGRO = 0, 1, 2
        color = {v: COLOR_BLANCO for v in self._lista}
        
        def dfs_ciclo(v) -> bool:
            color[v] = COLOR_GRIS
            for vecino, _ in self.vecinos(v):
                if color[vecino] == COLOR_GRIS:
                    return True  # arista al gris = ciclo
                if color[vecino] == COLOR_BLANCO and dfs_ciclo(vecino):
                    return True
            color[v] = COLOR_NEGRO
            return False
        
        for v in self._lista:
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

    # ------------------------------------------------------------------
    # Bellman-Ford (camino más corto, admite pesos negativos)
    # ------------------------------------------------------------------
    def bellman_ford(self, origen, destino):
        """Camino más corto entre dos vértices con el algoritmo de Bellman-Ford.

        A diferencia de Dijkstra, admite aristas con peso negativo. Relaja
        todas las aristas V-1 veces; si todavía se puede mejorar una distancia
        después de eso, existe un ciclo de peso negativo.

        Args:
            origen: Vértice de inicio.
            destino: Vértice de destino.

        Returns:
            tuple: (camino, distancia).
            None: Si algún vértice no existe o no hay camino.

        Raises:
            ValueError: Si hay un ciclo negativo alcanzable desde el origen.
        """
        if origen not in self._lista or destino not in self._lista:
            return None

        distancias = {v: float('inf') for v in self._lista}
        distancias[origen] = 0
        predecesores = {v: None for v in self._lista}

        # V-1 rondas: en cada una se relajan TODAS las aristas
        for _ in range(len(self._lista) - 1):
            hubo_cambio = False
            for u in self._lista:
                if distancias[u] == float('inf'):
                    continue  # todavía no se llega a u
                for v, peso in self.vecinos(u):
                    if distancias[u] + peso < distancias[v]:
                        distancias[v] = distancias[u] + peso
                        predecesores[v] = u
                        hubo_cambio = True
            if not hubo_cambio:
                break  # ya está estable, no hace falta seguir

        # Ronda extra: si aún mejora algo, hay ciclo negativo
        for u in self._lista:
            if distancias[u] == float('inf'):
                continue
            for v, peso in self.vecinos(u):
                if distancias[u] + peso < distancias[v]:
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
        if not self._lista:
            return [], 0

        # Reúne cada arista una sola vez (en no dirigido aparece u-v y v-u)
        aristas = []
        vistas = set()
        for u in self._lista:
            for v, peso in self._lista[u]:
                if (v, u) not in vistas:
                    aristas.append((peso, u, v))
                    vistas.add((u, v))
        aristas.sort(key=lambda a: a[0])

        # Union-Find: cada vértice empieza en su propio grupo
        padre = {v: v for v in self._lista}

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

        if len(mst) != len(self._lista) - 1:
            return None  # no conexo
        return mst, costo_total

    def prim(self, inicio=None):
        """Árbol de expansión de costo mínimo con el algoritmo de Prim.

        Parte de un vértice y en cada paso toma la arista más barata que
        conecta lo ya visitado con un vértice nuevo (usa un heap).

        Args:
            inicio: Vértice inicial (por defecto, el primero del grafo).

        Returns:
            tuple: (aristas, costo_total) con aristas como lista de (u, v, peso).
            None: Si el grafo es dirigido o no es conexo.
        """
        if self.dirigido:
            return None
        if not self._lista:
            return [], 0
        if inicio is None:
            inicio = next(iter(self._lista))
        if inicio not in self._lista:
            return None

        visitados = {inicio}
        heap = [(peso, inicio, v) for v, peso in self.vecinos(inicio)]
        heapq.heapify(heap)
        mst = []
        costo_total = 0

        while heap and len(visitados) < len(self._lista):
            peso, u, v = heapq.heappop(heap)
            if v in visitados:
                continue  # esa arista ya no aporta
            visitados.add(v)
            mst.append((u, v, peso))
            costo_total += peso
            for w, peso_w in self.vecinos(v):
                if w not in visitados:
                    heapq.heappush(heap, (peso_w, v, w))

        if len(visitados) != len(self._lista):
            return None  # no conexo
        return mst, costo_total