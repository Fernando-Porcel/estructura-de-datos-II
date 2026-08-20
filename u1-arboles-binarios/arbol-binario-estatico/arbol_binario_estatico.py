"""
Árbol Binario de Búsqueda (ABB) implementado de forma ESTÁTICA
usando un arreglo (lista de Python) en lugar de nodos enlazados.
 
Técnica: indexación implícita (la misma que usan los heaps)
    - Raíz en el índice 0
    - Para un nodo en el índice i:
        hijo_izquierdo = 2*i + 1
        hijo_derecho   = 2*i + 2
        padre          = (i - 1) // 2   (si i > 0)
"""


class ArbolBinarioEstatico:

    def __init__(self, capacidad_inicial=16):
        """
        Inicializa un árbol binario estático vacío.
        
        Args:
            capacidad_inicial (int): La capacidad máxima del arreglo. Por defecto es 16.
        
        Attributes:
            capacidad (int): La capacidad máxima del arreglo.
            arreglo (list): Lista inicializada con None en todas las posiciones.
        """
        self.capacidad = capacidad_inicial
        self.arreglo = [None] * self.capacidad

    # ---------- utilidades de índices ----------
    @staticmethod
    def hijo_izq(i):
        """
        Calcula el índice del hijo izquierdo de un nodo.
        
        Args:
            i (int): El índice del nodo padre.
        
        Returns:
            int: El índice del hijo izquierdo.
        """
        return 2 * i + 1

    @staticmethod
    def hijo_der(i):
        """
        Calcula el índice del hijo derecho de un nodo.
        
        Args:
            i (int): El índice del nodo padre.
        
        Returns:
            int: El índice del hijo derecho.
        """
        return 2 * i + 2
 
    @staticmethod
    def padre(i):
        """
        Calcula el índice del nodo padre.
        
        Args:
            i (int): El índice del nodo hijo (debe ser mayor a 0).
        
        Returns:
            int: El índice del nodo padre.
        """
        return (i - 1) // 2

    # ---------- inserción (estilo ABB) ----------
    def insertar(self, valor):
        """
        Inserta un nuevo valor en el árbol de forma ordenada.
        Si el valor ya existe, no se inserta duplicado.
        
        Args:
            valor: El valor a insertar en el árbol.
        
        Returns:
            bool: True si se insertó correctamente, False si el valor ya existía.
        """
        indice = 0
        while True:
            if self.arreglo[indice] is None:
                self.arreglo[indice] = valor
                return True
            if valor < self.arreglo[indice]:
                indice = self.hijo_izq(indice)
            elif valor > self.arreglo[indice]:
                indice = self.hijo_der(indice)
            else:
                return False  # valor duplicado, no se inserta

    # ---------- búsqueda ----------
    def buscar(self, valor):
        """
        Busca un valor en el árbol y retorna su índice si existe.
        
        Args:
            valor: El valor a buscar en el árbol.
        
        Returns:
            int: El índice del nodo si se encuentra, -1 si no existe.
        """
        indice = 0
        while indice < self.capacidad and self.arreglo[indice] is not None:
            actual = self.arreglo[indice]
            if valor == actual:
                return indice
            elif valor < actual:
                indice = self.hijo_izq(indice)
            else:
                indice = self.hijo_der(indice)
        return -1

    # ---------- recorridos ----------
    def inorden(self, indice=0, resultado=None):
        """
        Realiza un recorrido en-orden (izquierdo -> raíz -> derecho).
        Este recorrido produce los elementos en orden ascendente.
        
        Args:
            indice (int): El índice del nodo actual (por defecto 0, la raíz).
            resultado (list): Lista acumuladora para los valores del recorrido.
        
        Returns:
            list: Una lista con los valores del árbol en orden ascendente.
        """
        if resultado is None:
            resultado = []
        if indice < self.capacidad and self.arreglo[indice] is not None:
            self.inorden(self.hijo_izq(indice), resultado)
            resultado.append(self.arreglo[indice])
            self.inorden(self.hijo_der(indice), resultado)
        return resultado

    def preorden(self, indice=0, resultado=None):
        """
        Realiza un recorrido pre-orden (raíz -> izquierdo -> derecho).
        
        Args:
            indice (int): El índice del nodo actual (por defecto 0, la raíz).
            resultado (list): Lista acumuladora para los valores del recorrido.
        
        Returns:
            list: Una lista con los valores según el orden de visita.
        """
        if resultado is None:
            resultado = []
        if indice < self.capacidad and self.arreglo[indice] is not None:
            resultado.append(self.arreglo[indice])
            self.preorden(self.hijo_izq(indice), resultado)
            self.preorden(self.hijo_der(indice), resultado)
        return resultado

    def postorden(self, indice=0, resultado=None):
        """
        Realiza un recorrido post-orden (izquierdo -> derecho -> raíz).
        
        Args:
            indice (int): El índice del nodo actual (por defecto 0, la raíz).
            resultado (list): Lista acumuladora para los valores del recorrido.
        
        Returns:
            list: Una lista con los valores según el orden de visita.
        """
        if resultado is None:
            resultado = []
        if indice < self.capacidad and self.arreglo[indice] is not None:
            self.postorden(self.hijo_izq(indice), resultado)
            self.postorden(self.hijo_der(indice), resultado)
            resultado.append(self.arreglo[indice])
        return resultado