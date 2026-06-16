import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys

def configurar_tabla(columnas):
    """Configura dinámicamente las columnas del Treeview."""
    tabla["columns"] = columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=100)

def crear_input(texto_label, clave_diccionario):
    """Crea una fila con un Label y un Entry dinámicamente."""
    frame = tk.Frame(frame_inputs)
    frame.pack(side="top", fill="x", pady=2)
    tk.Label(frame, text=texto_label, width=20, anchor="e").pack(side="left", padx=5)
    entry = tk.Entry(frame)
    entry.pack(side="left", fill="x", expand=True, padx=5)
    entradas[clave_diccionario] = entry

def actualizar_inputs(event=None):
    """Actualiza los campos de texto según el método seleccionado."""
    for widget in frame_inputs.winfo_children():
        widget.destroy()
    entradas.clear()
    
    for fila in tabla.get_children():
        tabla.delete(fila)

    metodo = combo_metodo.get()

    if metodo == "Cuadrados Medios":
        crear_input("Semilla (4 dígitos):", "semilla")
    elif metodo == "Productos Medios":
        crear_input("Semilla 1 (4 dígitos):", "semilla1")
        crear_input("Semilla 2 (4 dígitos):", "semilla2")
    elif metodo == "Multiplicador Constante":
        crear_input("Constante (a):", "a")
        crear_input("Semilla (4 dígitos):", "semilla")
    elif metodo == "Congruencial Lineal":
        crear_input("Constante (a):", "a")
        crear_input("Constante (c):", "c")
        crear_input("Semilla:", "semilla")
        crear_input("Módulo (m):", "m")

def ejecutar_script_externo(nombre_archivo, lista_valores):
    """
    Ejecuta un archivo .py externo, le envía los inputs y captura los prints.
    """
    # Convertimos la lista de valores en un solo string separado por saltos de línea (como si el usuario presionara Enter)
    input_str = "\n".join(lista_valores) + "\n"
    
    try:
        # sys.executable asegura que usemos el mismo Python que está corriendo la ventana
        resultado = subprocess.run(
            [sys.executable, nombre_archivo],
            input=input_str,
            text=True,          # Para que devuelva texto y no bytes
            capture_output=True # Para capturar lo que el script "imprime"
        )
        
        # Procesar el texto impreso por el script
        lineas_impresas = resultado.stdout.split("\n")
        datos_tabla = []
        guardar = False
        
        for linea in lineas_impresas:
            # Buscamos la línea de guiones que usaste en tus print ("-" * 50)
            if set(linea.strip()) == {"-"}:
                guardar = True
                continue
            
            # Si estamos después de la línea de guiones y la línea no está vacía
            if guardar and linea.strip():
                # Dividimos la línea por sus espacios en blanco para obtener las columnas
                columnas = linea.split()
                datos_tabla.append(columnas)
                
        return datos_tabla
    
    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"No se pudo ejecutar {nombre_archivo}.\nDetalle: {e}")
        return []

def generar():
    """Recopila los datos y llama a ejecutar_script_externo."""
    for fila in tabla.get_children():
        tabla.delete(fila)

    metodo = combo_metodo.get()
    
    try:
        if metodo == "Cuadrados Medios":
            val_semilla = entradas["semilla"].get()
            configurar_tabla(("Iter", "Semilla", "Cuadrado", "Centro", "Ri"))
            
            # Tu archivo cuadrados_medios.py pide 1 dato
            filas = ejecutar_script_externo("cuadrados_medios.py", [val_semilla])

        elif metodo == "Productos Medios":
            val_semilla1 = entradas["semilla1"].get()
            val_semilla2 = entradas["semilla2"].get()
            configurar_tabla(("Iter", "Semilla", "Semilla2", "Producto", "Centro", "Ri"))
            
            # Tu archivo productos_medios.py pide 2 datos
            filas = ejecutar_script_externo("productos_medios.py", [val_semilla1, val_semilla2])

        elif metodo == "Multiplicador Constante":
            val_a = entradas["a"].get()
            val_semilla = entradas["semilla"].get()
            configurar_tabla(("Iter", "Constante", "Semilla", "Resultado", "Centro", "Ri"))
            
            
            # Tu archivo multiplicador_contacto.py pide 2 datos (Constante y luego Semilla)
            filas = ejecutar_script_externo("multiplicador_contacto.py", [val_a, val_semilla])

        elif metodo == "Congruencial Lineal":
            val_a = entradas["a"].get()
            val_c = entradas["c"].get()
            val_semilla = entradas["semilla"].get()
            val_m = entradas["m"].get()
            configurar_tabla(("Iter", "Semilla", "Resultado", "Ri"))
            
            # Tu archivo otro.py pide 4 datos (a, c, semilla, modulo)
            filas = ejecutar_script_externo("otro.py", [val_a, val_c, val_semilla, val_m])

        # Rellenar la tabla con los datos extraídos
        if filas:
            for fila in filas:
                tabla.insert("", "end", values=fila)
        else:
            messagebox.showwarning("Sin datos", "El script no devolvió datos. Asegúrate de que los archivos estén en la misma carpeta.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


# --- Configuración de la Ventana Principal ---
ventana = tk.Tk()
ventana.title("Generador (Leyendo archivos originales)")
ventana.geometry("800x450")

entradas = {}

# Panel Superior
frame_metodo = tk.Frame(ventana)
frame_metodo.pack(pady=10)

tk.Label(frame_metodo, text="Seleccione el Método:").pack(side="left", padx=5)
opciones_metodos = [
    "Cuadrados Medios", 
    "Productos Medios", 
    "Multiplicador Constante", 
    "Congruencial Lineal"
]
combo_metodo = ttk.Combobox(frame_metodo, values=opciones_metodos, state="readonly", width=30)
combo_metodo.set("Cuadrados Medios")
combo_metodo.pack(side="left", padx=5)

# Panel de Inputs
frame_inputs = tk.Frame(ventana)
frame_inputs.pack(pady=10, fill="x", padx=150)

# Botón Generar
tk.Button(ventana, text="Ejecutar Archivo y Mostrar", command=generar, bg="#008CBA", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

# Panel Inferior: Tabla
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

scroll_y = ttk.Scrollbar(frame_tabla)
scroll_y.pack(side="right", fill="y")

tabla = ttk.Treeview(frame_tabla, show="headings", yscrollcommand=scroll_y.set)
scroll_y.config(command=tabla.yview)
tabla.pack(fill="both", expand=True)

# Eventos
combo_metodo.bind("<<ComboboxSelected>>", actualizar_inputs)
actualizar_inputs()

ventana.mainloop()