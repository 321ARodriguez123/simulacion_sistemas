def generar(a, c, semilla, m, rango):
    filas = []
    ri_list = []
    for i in range(1, rango + 1):
        resultado = (a * semilla + c) % m
        ri = resultado / m
        filas.append((i, semilla, resultado, f"{ri:.4f}"))
        ri_list.append(ri)
        semilla = resultado
    return filas, ri_list