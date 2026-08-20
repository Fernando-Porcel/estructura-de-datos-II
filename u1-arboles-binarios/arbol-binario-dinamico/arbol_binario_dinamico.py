from nodo import Nodo


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
                return Nodo(valor)
            
            if valor < nodo.valor:
                nodo.izquierdo = self._insertar_recursivo(valor, nodo.izquierdo)
            elif valor > nodo.valor:
                nodo.derecho = self._insertar_recursivo(valor, nodo.derecho)
    
            return nodo

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