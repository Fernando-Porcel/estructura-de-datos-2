from arbol_MVias import ArbolMvia

def ejemplo():
    arbol = ArbolMvia(4)
    arbol.insertar(10)
    arbol.insertar(20)
    arbol.insertar(30)
    arbol.insertar(5)
    arbol.insertar(8)
    arbol.insertar(22)
    arbol.insertar(25)
    arbol.insertar(32)
    arbol.insertar(40)

    print("Estadisticas:")
    print(f"Buscar 30: {arbol.buscar(30)}")
    print(f"Cantidad: {arbol.cantidad()}")
    print(f"Amplitud: {arbol.amplitud()}")
    print(f"Altura: {arbol.altura()}")

    print("\nRecorridos:")
    print(f"en-orden: {arbol.en_orden()}")
    print(f"pre-orden: {arbol.pre_orden()}")
    print(f"pos-orden: {arbol.pos_orden()}")
    print(f"por-nivel: {arbol.por_nivel()}")

if __name__ == "__main__":
    ejemplo()