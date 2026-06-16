def RI__(numero):
    x = numero/999

    return x


a = int(input("Ingrese constante 1: "))
c = int(input("Ingrese constante 2: "))
semilla = int(input("Ingrese una semilla: "))
m = int(input("Ingrese el modulo: "))

print("{:<5} {:<10} {:<12} {:<8}".format(
    "Iter", "Semilla", "Resultado", "Ri"
))

print("-" * 50)

for i in range(1, 7):

    resultado = (a * semilla + c) % m

    ri_ = RI__(resultado)

    print("{:<5} {:<10} {:<12} {:.4f}".format(
        i,
        semilla,
        resultado,
        ri_
    ))

    semilla = resultado