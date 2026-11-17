from grafo_lista import GrafoLista
from grafo_matriz import GrafoMatriz

GrafoLista = GrafoLista(True)
GrafoMatriz = GrafoMatriz(True)

GrafoLista.agregar_arista('A', 'B')
GrafoLista.agregar_arista('A', 'C')
GrafoLista.agregar_arista('C', 'B')
GrafoLista.agregar_arista('B', 'D')

GrafoLista.mostrar_lista()
print(GrafoLista.dfs('A'))
print(GrafoLista.bfs('A'))
print(GrafoLista.camino_mas_corto('A', 'D'))