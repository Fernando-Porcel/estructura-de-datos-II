# limpiar_datos.py
import pandas as pd
from models.ml_agent import COLUMNAS

df = pd.read_csv('dataset.csv')

print('Filas:', len(df))
print('Valores nulos:', df.isnull().sum().sum())
print('Filas repetidas:', df.duplicated().sum())
print('Tableros únicos:', len(df.drop_duplicates(subset=COLUMNAS)))

# Un mismo tablero no debería tener dos jugadas distintas (Minimax es determinista)
conflictos = df.drop_duplicates().duplicated(subset=COLUMNAS).sum()
print('Tableros con etiquetas distintas:', conflictos)

# La jugada elegida debe caer en una casilla vacía (valor 0)
def jugada_valida(fila):
    return fila[f"casilla_{int(fila['jugada'])}"] == 0

print('Jugadas inválidas:', (~df.apply(jugada_valida, axis=1)).sum())

df_limpio = df.drop_duplicates(subset=COLUMNAS).reset_index(drop=True)
df_limpio.to_csv('dataset_limpio.csv', index=False)
print('Dataset limpio:', df_limpio.shape)