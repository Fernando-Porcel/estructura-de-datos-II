import random

class AgenteMinimax:
    def __init__(self, jugador_ia='O', jugador_humano='X', profundidad_maxima=None):
        self.jugador_ia = jugador_ia
        self.jugador_humano = jugador_humano
        self.profundidad_maxima = profundidad_maxima   # None = sin límite (imbatible)
        self.nodos_evaluados = 0   # contador para ver cuánto trabaja el algoritmo

    def evaluar(self, tablero):
        """Puntaje de un tablero: +10 si gana la IA, -10 si gana el humano, 0 en otro caso."""
        if tablero.hay_ganador(self.jugador_ia):
            return 10
        elif tablero.hay_ganador(self.jugador_humano):
            return -10
        return 0

    def minimax(self, tablero, profundidad, es_maximizador):
        self.nodos_evaluados += 1
        puntaje = self.evaluar(tablero)

        # Casos base: el juego terminó (hojas del árbol)
        if puntaje == 10:
            return puntaje - profundidad
        if puntaje == -10:
            return puntaje + profundidad
        if not tablero.obtener_movimientos_disponibles():
            return 0   # tablero lleno sin ganador: empate

        # Límite de profundidad (dificultad): la IA no mira más allá y valora la posición como 0
        if self.profundidad_maxima is not None and profundidad >= self.profundidad_maxima:
            return 0

        if es_maximizador:
            mejor_puntaje = -float('inf')
            for movimiento in tablero.obtener_movimientos_disponibles():
                tablero.realizar_movimiento(movimiento, self.jugador_ia)             # 1. hacer
                puntaje_actual = self.minimax(tablero, profundidad + 1, False)       # 2. explorar
                tablero.deshacer_movimiento(movimiento)                              # 3. deshacer (BACKTRACKING)
                mejor_puntaje = max(mejor_puntaje, puntaje_actual)
        else:
            mejor_puntaje = float('inf')
            for movimiento in tablero.obtener_movimientos_disponibles():
                tablero.realizar_movimiento(movimiento, self.jugador_humano)         # 1. hacer
                puntaje_actual = self.minimax(tablero, profundidad + 1, True)        # 2. explorar
                tablero.deshacer_movimiento(movimiento)                              # 3. deshacer (BACKTRACKING)
                mejor_puntaje = min(mejor_puntaje, puntaje_actual)

        return mejor_puntaje

    def obtener_mejor_movimiento(self, tablero):
        self.nodos_evaluados = 0
        mejor_puntaje = -float('inf')
        mejores = []   # todas las jugadas que empatan en el mejor puntaje

        for movimiento in tablero.obtener_movimientos_disponibles():
            tablero.realizar_movimiento(movimiento, self.jugador_ia)
            puntaje = self.minimax(tablero, 1, False)
            tablero.deshacer_movimiento(movimiento)

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejores = [movimiento]
            elif puntaje == mejor_puntaje:
                mejores.append(movimiento)

        # Sin límite de profundidad: siempre la primera (determinista; lo necesita el dataset).
        # Con límite (fácil / medio): entre las empatadas se elige una al azar.
        if self.profundidad_maxima is None:
            return mejores[0]
        return random.choice(mejores)

