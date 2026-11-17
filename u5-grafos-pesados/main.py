from grafo_pesado_lista import GrafoPesadoLista
from grafo_pesado_matriz import GrafoPesadoMatriz

GrafoLista = GrafoPesadoLista(True)
GrafoMatriz = GrafoPesadoMatriz(True)

GrafoLista.agregar_arista('A', 'B', 4)
GrafoLista.agregar_arista('A', 'C', 1)
GrafoLista.agregar_arista('C', 'B', 2)
GrafoLista.agregar_arista('B', 'D', 5)

GrafoLista.mostrar_lista()
print(GrafoLista.dfs('A'))
print(GrafoLista.bfs('A'))
print(GrafoLista.dijkstra('A', 'D'))