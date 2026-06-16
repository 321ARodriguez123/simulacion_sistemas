import tkinter as tk
from tkinter import ttk


def obtener_centro(numero):

    texto = str(numero)

    if len(texto) % 2 == 1:
        texto = "0" + texto

    inicio = (len(texto) - 4) // 2

    return texto[inicio:inicio + 4]


def generar():

    # Limpiar tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    semilla = int(txt_semilla.get())

    for i in range(1, 7):

        cuadrado = semilla ** 2

        centro = obtener_centro(cuadrado)

        ri = int(centro) / 10000

        tabla.insert(
            "",
            "end",
            values=(
                i,
                semilla,
                cuadrado,
                centro,
                f"{ri:.4f}"
            )
        )

        semilla = int(centro)


# Ventana principal
ventana = tk.Tk()
ventana.title("Metodo de Cuadrados Medios")
ventana.geometry("700x300")

# Etiqueta
tk.Label(
    ventana,
    text="Semilla:"
).pack(pady=5)

# Caja de texto
txt_semilla = tk.Entry(ventana)
txt_semilla.pack()

# Botón
tk.Button(
    ventana,
    text="Generar",
    command=generar
).pack(pady=10)

# Tabla
columnas = (
    "Iteracion",
    "Semilla",
    "Cuadrado",
    "Centro",
    "Ri"
)

tabla = ttk.Treeview(
    ventana,
    columns=columnas,
    show="headings"
)

for col in columnas:
    tabla.heading(col, text=col)

tabla.pack(fill="both", expand=True)

ventana.mainloop()