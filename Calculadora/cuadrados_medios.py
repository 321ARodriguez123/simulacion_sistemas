def obtener_centro(numero):
    texto = str(numero).zfill(4)
    if len(texto) % 2 == 1:
        texto = "0" + texto
    inicio = (len(texto) - 4) // 2
    return texto[inicio:inicio + 4]

def generar(semilla, rango):
    filas = []
    ri_list = []
    for i in range(1, rango + 1):
        cuadrado = semilla ** 2
        centro = obtener_centro(cuadrado)
        ri = int(centro) / 10000
        filas.append((i, semilla, cuadrado, centro, f"{ri:.4f}"))
        ri_list.append(ri)
        semilla = int(centro)
    return filas, ri_list