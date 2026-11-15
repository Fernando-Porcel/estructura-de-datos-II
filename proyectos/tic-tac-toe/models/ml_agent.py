# models/ml_agent.py
import random
import joblib
import joblib
import pandas as pd

from models.game_model import Tablero

# Código numérico de cada ficha. Es arbitrario, pero debe ser SIEMPRE el mismo
# al entrenar y al predecir.
CODIGO_FICHA = {'X': 1, 'O': -1, ' ': 0}

# Nombres de las 9 columnas de características del dataset
COLUMNAS = [f'casilla_{i}' for i in range(9)]


def tablero_a_vector(tablero):
    """Convierte el tablero 3x3 en una lista de 9 números (fila por fila)."""
    vector = []
    for fila in tablero.casillas:
        for ficha in fila:
            vector.append(CODIGO_FICHA[ficha])
    return vector


def movimiento_a_indice(movimiento):
    """(fila, columna) -> número del 0 al 8."""
    fila, columna = movimiento
    return fila * 3 + columna


def indice_a_movimiento(indice):
    """Número del 0 al 8 -> (fila, columna)."""
    return divmod(indice, 3)


# ---------------------------------------------------------------------------
# Generación del dataset
# ---------------------------------------------------------------------------

class ConsultorMinimax:
    """Le pregunta a Minimax y recuerda las respuestas para no recalcularlas."""

    def __init__(self, agente):
        self.agente = agente
        self.memoria = {}   # {tablero (tupla de 9 números): mejor jugada}

    def mejor_movimiento(self, tablero):
        clave = tuple(tablero_a_vector(tablero))
        if clave not in self.memoria:
            self.memoria[clave] = self.agente.obtener_mejor_movimiento(tablero)
        return self.memoria[clave]


def simular_partida(consultor):
    """X juega al azar y O juega con Minimax.
    Devuelve las decisiones de la IA como una lista de (vector del tablero, índice de la jugada)."""
    tablero = Tablero()
    muestras = []
    turno = 'X'

    while True:
        if turno == 'X':
            movimiento = random.choice(tablero.obtener_movimientos_disponibles())
        else:
            movimiento = consultor.mejor_movimiento(tablero)
            # Anotamos ANTES de jugar: el tablero tal como lo vio la IA
            muestras.append((tablero_a_vector(tablero), movimiento_a_indice(movimiento)))

        tablero.realizar_movimiento(movimiento, turno)

        if tablero.hay_ganador(turno) or tablero.hay_empate():
            return muestras
        turno = 'O' if turno == 'X' else 'X'


def generar_dataset(num_partidas, consultor):
    """Simula varias partidas y devuelve un DataFrame:
    9 columnas con el tablero (casilla_0 ... casilla_8) y la columna 'jugada' (la etiqueta)."""
    filas = []
    for _ in range(num_partidas):
        for vector, indice in simular_partida(consultor):
            filas.append(vector + [indice])
    return pd.DataFrame(filas, columns=COLUMNAS + ['jugada'])


# ---------------------------------------------------------------------------
# Agente que juega con el árbol de decisión entrenado
# ---------------------------------------------------------------------------

class AgenteML:
    """Juega con el árbol de decisión entrenado. No explora nada: solo consulta el modelo."""

    def __init__(self, ruta_modelo='modelo_arbol.joblib'):
        self.modelo = joblib.load(ruta_modelo)

    def obtener_mejor_movimiento(self, tablero):
        entrada = pd.DataFrame([tablero_a_vector(tablero)], columns=COLUMNAS)
        movimiento = indice_a_movimiento(int(self.modelo.predict(entrada)[0]))

        disponibles = tablero.obtener_movimientos_disponibles()
        if movimiento in disponibles:
            return movimiento

        # El árbol propuso una casilla ocupada: usamos la primera casilla libre
        return disponibles[0]