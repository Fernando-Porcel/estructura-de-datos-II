# entrenar.py
import pandas as pd
import joblib

from sklearn.tree import export_text
from sklearn.tree import DecisionTreeClassifier
from models.ml_agent import COLUMNAS

df = pd.read_csv('dataset_limpio.csv')

X = df[COLUMNAS]      # características: las 9 casillas
y = df['jugada']      # etiqueta: la jugada que eligió Minimax

modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X, y)

print('Profundidad del árbol:', modelo.get_depth())
print('Número de hojas:', modelo.get_n_leaves())
print('Acierto sobre los datos de entrenamiento:', modelo.score(X, y))

# Una consulta: X en el centro, el resto vacío
tablero = pd.DataFrame([[0, 0, 0, 0, 1, 0, 0, 0, 0]], columns=COLUMNAS)
print('Jugada predicha:', modelo.predict(tablero))

reglas = export_text(modelo, feature_names=COLUMNAS, max_depth=3)
print(reglas)

joblib.dump(modelo, 'modelo_arbol.joblib')