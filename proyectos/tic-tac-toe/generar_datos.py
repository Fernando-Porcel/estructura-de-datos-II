# generar_datos.py
from models.minimax_agent import AgenteMinimax
from models.ml_agent import ConsultorMinimax, generar_dataset, COLUMNAS

consultor = ConsultorMinimax(AgenteMinimax())
df = generar_dataset(1000, consultor)
df.to_csv('dataset.csv', index=False)

print(df.shape)
print(df.head())
print('Filas únicas:', len(df.drop_duplicates()))
print('Tableros únicos:', len(df.drop_duplicates(subset=COLUMNAS)))
print(df['jugada'].value_counts())