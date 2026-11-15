# modelo/modelo_juego.py

class Tablero:
    def __init__(self, casillas=None):
        if casillas is None:
            # Tablero nuevo: matriz 3x3 vacía
            self.casillas = [[' ' for _ in range(3)] for _ in range(3)]
        else:
            # Tablero reconstruido a partir de una matriz existente
            self.casillas = [fila[:] for fila in casillas]

    # Las 8 líneas con las que se puede ganar (cada una son 3 casillas)
    LINEAS_GANADORAS = [
        # Filas
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columnas
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonales
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def obtener_casillas(self):
        """Devuelve una copia de la matriz, lista para guardar en la sesión."""
        return [fila[:] for fila in self.casillas]

    def obtener_movimientos_disponibles(self):
        """Devuelve una lista de (fila, columna) con las casillas vacías."""
        movimientos = []
        for fila in range(3):
            for columna in range(3):
                if self.casillas[fila][columna] == ' ':
                    movimientos.append((fila, columna))
        return movimientos

    def realizar_movimiento(self, movimiento, jugador):
        """Coloca la ficha del jugador ('X' u 'O') en la casilla indicada."""
        fila, columna = movimiento
        self.casillas[fila][columna] = jugador

    def deshacer_movimiento(self, movimiento):
        """Deshace la jugada: deja la casilla vacía otra vez."""
        fila, columna = movimiento
        self.casillas[fila][columna] = ' '

    def hay_ganador(self, jugador):
        """Devuelve True si el jugador ('X' u 'O') completó alguna línea."""
        for linea in self.LINEAS_GANADORAS:
            if all(self.casillas[fila][columna] == jugador for fila, columna in linea):
                return True
        return False

    def hay_empate(self):
        """Empate: no quedan movimientos y ninguno de los dos ganó."""
        return (not self.obtener_movimientos_disponibles()
                and not self.hay_ganador('X')
                and not self.hay_ganador('O'))

    def __str__(self):
        filas = [' | '.join(fila) for fila in self.casillas]
        return '\n---------\n'.join(filas)