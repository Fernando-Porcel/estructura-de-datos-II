from arbol_binario_dinamico import ArbolBinario

arbol = ArbolBinario()
infija = input("Ingrese una expresion infija: ")
arbol.construir(infija)
postfija = " ".join(arbol.post_orden())
print(postfija)