import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# IMPORTAMOS NUESTROS PROPIOS ARCHIVOS
# ==========================================
import cuadrados_medios
import productos_medios
import multiplicador_contacto
import otro
import uni_var_media
import graficos  # <-- NUEVO ARCHIVO IMPORTADO

class AplicacionSimulacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador y Evaluador de Números Pseudoaleatorios")
        self.root.geometry("1000x600")
        
        self.entradas = {}
        self.metodo_actual = tk.StringVar(value="Cuadrados Medios")
        
        # Guardará la lista de Ri generados en la iteración actual
        self.ri_actual = [] # <-- NUEVA VARIABLE PARA LOS GRÁFICOS
        
        self.construir_interfaz()
        self.actualizar_inputs()

    def construir_interfaz(self):
        # --- BARRA LATERAL ---
        sidebar = tk.Frame(self.root, width=200, bg="#2c3e50", relief="sunken")
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="MÉTODOS", fg="white", bg="#2c3e50", font=("Arial", 12, "bold")).pack(pady=20)
        
        opciones = ["Cuadrados Medios", "Productos Medios", "Multiplicador Constante", "Congruencial Lineal"]
        for op in opciones:
            rb = tk.Radiobutton(
                sidebar, text=op, variable=self.metodo_actual, value=op,
                command=self.actualizar_inputs, bg="#2c3e50", fg="white", 
                selectcolor="#34495e", activebackground="#2c3e50",
                font=("Arial", 10), indicatoron=0, width=20, pady=10
            )
            rb.pack(pady=5, padx=10)

        # --- ÁREA PRINCIPAL ---
        area_principal = tk.Frame(self.root)
        area_principal.pack(side="right", fill="both", expand=True)

        self.frame_inputs = tk.Frame(area_principal, pady=15)
        self.frame_inputs.pack(fill="x")
        
        # CONTENEDOR DE BOTONES (Modificado para alinear los dos botones)
        frame_botones = tk.Frame(area_principal)
        frame_botones.pack(pady=5)
        
        tk.Button(frame_botones, text="Generar y Evaluar", command=self.generar, bg="#27ae60", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        
        # NUEVO BOTÓN PARA LOS GRÁFICOS
        tk.Button(frame_botones, text="Ver Gráficos 📊", command=self.mostrar_graficos, bg="#2980b9", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        panel_dividido = tk.PanedWindow(area_principal, orient="horizontal")
        panel_dividido.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabla
        frame_tabla = tk.Frame(panel_dividido)
        panel_dividido.add(frame_tabla, minsize=400)
        scroll_y = ttk.Scrollbar(frame_tabla)
        scroll_y.pack(side="right", fill="y")
        self.tabla = ttk.Treeview(frame_tabla, show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tabla.yview)
        self.tabla.pack(fill="both", expand=True)

        # Panel Estadístico
        frame_stats = tk.Frame(panel_dividido, bg="#ecf0f1", padx=10, pady=10)
        panel_dividido.add(frame_stats, minsize=250)
        tk.Label(frame_stats, text="Resultados Estadísticos", bg="#ecf0f1", font=("Arial", 11, "bold")).pack(anchor="w")
        self.texto_stats = tk.Text(frame_stats, width=40, height=20, font=("Courier", 10), bg="#f9f9f9", state="disabled")
        self.texto_stats.pack(fill="both", expand=True, pady=5)

    def crear_input(self, texto_label, clave_diccionario):
        frame = tk.Frame(self.frame_inputs)
        frame.pack(side="top", fill="x", pady=2)
        tk.Label(frame, text=texto_label, width=20, anchor="e").pack(side="left", padx=5)
        entry = tk.Entry(frame)
        entry.pack(side="left", fill="x", expand=True, padx=20)
        self.entradas[clave_diccionario] = entry

    def configurar_tabla(self, columnas):
        self.tabla["columns"] = columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=80)

    def actualizar_inputs(self):
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()
        self.entradas.clear()
        
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
            
        self.ri_actual = [] # Limpiar los datos acumulados al cambiar de método
            
        self.texto_stats.config(state="normal")
        self.texto_stats.delete(1.0, tk.END)
        self.texto_stats.insert(tk.END, "Esperando datos...")
        self.texto_stats.config(state="disabled")

        metodo = self.metodo_actual.get()
        if metodo == "Cuadrados Medios":
            self.crear_input("Semilla (4 dígitos):", "semilla")
            self.crear_input("Rango (Iteraciones):", "rango")
        elif metodo == "Productos Medios":
            self.crear_input("Semilla 1 (4 dígitos):", "semilla1")
            self.crear_input("Semilla 2 (4 dígitos):", "semilla2")
            self.crear_input("Rango (Iteraciones):", "rango")
        elif metodo == "Multiplicador Constante":
            self.crear_input("Constante (a):", "a")
            self.crear_input("Semilla (4 dígitos):", "semilla")
            self.crear_input("Rango (Iteraciones):", "rango")
        elif metodo == "Congruencial Lineal":
            self.crear_input("Constante (a):", "a")
            self.crear_input("Constante (c):", "c")
            self.crear_input("Módulo (m):", "m")
            self.crear_input("Semilla:", "semilla")
            self.crear_input("Rango (Iteraciones):", "rango")

    def generar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        metodo = self.metodo_actual.get()
        filas = []
        ri_list = []
        
        try:
            rango = int(self.entradas["rango"].get())
            
            if metodo == "Cuadrados Medios":
                semilla = int(self.entradas["semilla"].get())
                self.configurar_tabla(("Iter", "Semilla", "Cuadrado", "Centro", "Ri"))
                filas, ri_list = cuadrados_medios.generar(semilla, rango)

            elif metodo == "Productos Medios":
                semilla1 = int(self.entradas["semilla1"].get())
                semilla2 = int(self.entradas["semilla2"].get())
                self.configurar_tabla(("Iter", "Semilla 1", "Semilla 2", "Producto", "Centro", "Ri"))
                filas, ri_list = productos_medios.generar(semilla1, semilla2, rango)

            elif metodo == "Multiplicador Constante":
                a = int(self.entradas["a"].get())
                semilla = int(self.entradas["semilla"].get())
                self.configurar_tabla(("Iter", "Constante", "Semilla", "Resultado", "Centro", "Ri"))
                filas, ri_list = multiplicador_contacto.generar(a, semilla, rango)

            elif metodo == "Congruencial Lineal":
                a = int(self.entradas["a"].get())
                c = int(self.entradas["c"].get())
                m = int(self.entradas["m"].get())
                semilla = int(self.entradas["semilla"].get())
                self.configurar_tabla(("Iter", "Semilla", "Resultado", "Ri"))
                filas, ri_list = otro.generar(a, c, semilla, m, rango)

            # Guardar en el estado de la clase para que el botón de gráficos tenga acceso
            self.ri_actual = ri_list # <-- NUEVO

            # Llenar la tabla
            for fila in filas:
                self.tabla.insert("", "end", values=fila)
                
            if ri_list:
                reporte = uni_var_media.reporte_simulacion(ri_list)
                self.texto_stats.config(state="normal")
                self.texto_stats.delete(1.0, tk.END)
                self.texto_stats.insert(tk.END, reporte)
                self.texto_stats.config(state="disabled")

        except ValueError:
            messagebox.showerror("Error", "Ingresa únicamente números enteros válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    # NUEVO MÉTODO PARA MANEJAR EL EVENTO DEL BOTÓN
    def mostrar_graficos(self):
        """Invoca la ventana del archivo externo pasándole el entorno principal y los datos."""
        graficos.abrir_ventana_graficos(self.root, self.ri_actual)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionSimulacion(root)
    root.mainloop()