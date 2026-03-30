from arbol_binario import ArbolBinario

def ejecutar_ejemplo():
    
    arbol = ArbolBinario()

    arbol.insertar(100)
    arbol.insertar(50)
    arbol.insertar(150)
    arbol.insertar(25)
    arbol.insertar(75)
    arbol.insertar(125)
    arbol.insertar(175)
    arbol.insertar(70)
    arbol.insertar(60)
    arbol.insertar(71)

    print(f"Cantidad: {arbol.cantidad()}")
    print(f"Buscar: {arbol.buscar(70)}")
    print(f"Buscar: {arbol.buscar(40)}")
    print(f"Ambplitud: {arbol.amplitud()}")
    print(f"Altura: {arbol.altura()}\n")

    arbol.imprimir()
    print("----------------------------------")
    arbol.eliminar(70)
    arbol.imprimir()
    print("----------------------------------")
    print(f"Cantidad: {arbol.cantidad()}")

if __name__ == "__main__":
    ejecutar_ejemplo()