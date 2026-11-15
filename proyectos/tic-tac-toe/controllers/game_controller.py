# controllers/game_controller.py
import time

from models.game_model import Tablero
from models.minimax_agent import AgenteMinimax
from models.ml_agent import AgenteML


class ControladorJuego:
    MODO_HUMANO = 'humano_vs_humano'
    MODO_MINIMAX = 'humano_vs_minimax'
    MODO_ML = 'humano_vs_ml'
    # Dificultad del modo Minimax: profundidad máxima de búsqueda (None = sin límite)
    DIFICULTADES = {'facil': 1, 'medio': 2, 'dificil': None}

    def __init__(self):
        # La IA siempre juega con 'O'; el humano con 'X'
        self.agentes_minimax = {
            nombre: AgenteMinimax(jugador_ia='O', jugador_humano='X', profundidad_maxima=profundidad)
            for nombre, profundidad in self.DIFICULTADES.items()
        }
        self.agente_ml = AgenteML()

    def nueva_partida(self, modo, dificultad='dificil'):
        """Devuelve el estado inicial de una partida."""
        if modo not in (self.MODO_HUMANO, self.MODO_MINIMAX, self.MODO_ML):
            raise ValueError(f'Modo desconocido: {modo}')
        if modo == self.MODO_MINIMAX and dificultad not in self.DIFICULTADES:
            raise ValueError(f'Dificultad desconocida: {dificultad}')

        return {
            'casillas': Tablero().obtener_casillas(),
            'turno': 'X',
            'modo': modo,
            'dificultad': dificultad if modo == self.MODO_MINIMAX else None,
            'ganador': None,
            'empate': False,
            'mensaje': 'Turno de X',
            'nodos': 0,
            'tiempo': 0,
        }

    def jugar(self, estado, fila, columna):
        """Aplica la jugada del humano y, si corresponde, la respuesta de la IA."""
        if estado['ganador'] or estado['empate']:
            return estado

        tablero = Tablero(estado['casillas'])

        if (fila, columna) not in tablero.obtener_movimientos_disponibles():
            estado['mensaje'] = 'Esa casilla no está disponible'
            return estado

        self._aplicar_movimiento(estado, tablero, (fila, columna))

        # Si la partida sigue y se juega contra la IA, le toca responder
        partida_en_curso = not (estado['ganador'] or estado['empate'])
        if estado['modo'] in (self.MODO_MINIMAX, self.MODO_ML) and partida_en_curso:
            self._jugar_ia(estado, tablero)

        return estado

    def _aplicar_movimiento(self, estado, tablero, movimiento):
        """Pone la ficha del jugador en turno y actualiza el estado."""
        jugador = estado['turno']
        tablero.realizar_movimiento(movimiento, jugador)
        estado['casillas'] = tablero.obtener_casillas()

        if tablero.hay_ganador(jugador):
            estado['ganador'] = jugador
            estado['mensaje'] = f'¡Ganó {jugador}!'
        elif tablero.hay_empate():
            estado['empate'] = True
            estado['mensaje'] = 'Empate'
        else:
            estado['turno'] = 'O' if jugador == 'X' else 'X'
            estado['mensaje'] = f"Turno de {estado['turno']}"

    def _jugar_ia(self, estado, tablero):
        """La IA elige su jugada (Minimax o árbol ML); medimos nodos y tiempo."""
        inicio = time.perf_counter()
        if estado['modo'] == self.MODO_ML:
            movimiento = self.agente_ml.obtener_mejor_movimiento(tablero)
            estado['nodos'] = 0     # el árbol no explora nodos
        else:
            agente = self.agentes_minimax[estado.get('dificultad') or 'dificil']
            movimiento = agente.obtener_mejor_movimiento(tablero)
            estado['nodos'] = agente.nodos_evaluados
        fin = time.perf_counter()

        estado['tiempo'] = round(fin - inicio, 4)
        self._aplicar_movimiento(estado, tablero, movimiento)