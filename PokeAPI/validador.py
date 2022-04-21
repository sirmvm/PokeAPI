import menu as o
def validador(op):
    opciones = ["2", "1"]
    while op not in opciones:
        print("### La opción ingresada no es válida ###\n\n")
        op=o.menu()
    return op