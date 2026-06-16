def obtener_centro(numero):
    texto = str(numero)

    if len(texto) % 2 == 1:
        texto = "0" + texto

    inicio = (len(texto) - 4) // 2

    return texto[inicio:inicio + 4]

a = int(input("Ingrese constante: "))
semilla = int(input("Ingrese una semilla: "))

print("{:<5} {:<10} {:<10} {:<12} {:<8} {:<10}".format(
    "Iter", "Constante", "Semilla", "Resultado", "Centro", "Ri"
))

print("-" * 50)

for i in range(1, 7):

    resultado = semilla * a

    centro = obtener_centro(resultado)

    ri = int(centro) / 10000

    print("{:<5} {:<10} {:<10} {:<12} {:<8} {:.4f}".format(
        i,
        a,
        semilla,
        resultado,
        centro,
        ri
    ))

    semilla = int(centro)