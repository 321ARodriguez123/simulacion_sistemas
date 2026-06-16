def obtener_centro(numero):
    texto = str(numero)

    if len(texto) % 2 == 1:
        texto = "0" + texto

    inicio = (len(texto) - 4) // 2

    return texto[inicio:inicio + 4]


semilla = int(input("Ingrese una semilla de 4 digitos: "))

print("{:<5} {:<10} {:<12} {:<8} {:<10}".format(
    "Iter", "Semilla", "Cuadrado", "Centro", "Ri"
))

print("-" * 50)

for i in range(1, 7):

    cuadrado = semilla ** 2

    centro = obtener_centro(cuadrado)

    ri = int(centro) / 10000

    print("{:<5} {:<10} {:<12} {:<8} {:.4f}".format(
        i,
        semilla,
        cuadrado,
        centro,
        ri
    ))

    semilla = int(centro)