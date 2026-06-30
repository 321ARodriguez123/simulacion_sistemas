import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import norm

class VentanaGraficos:
    def __init__(self, root_principal, datos_ri):
        # Convertimos la lista a un arreglo de numpy para hacer cálculos matemáticos rápidos
        self.datos_ri = np.array(datos_ri) 
        
        self.ventana = tk.Toplevel(root_principal)
        self.ventana.title("Análisis y Transformación de Distribuciones")
        self.ventana.geometry("1000x600")
        self.ventana.configure(bg="#f5f6fa")
        self.ventana.transient(root_principal)
        self.ventana.focus_set()

        # Variable para saber qué distribución seleccionó el usuario
        self.dist_actual = tk.StringVar(value="Uniforme (0, 1) - Original")
        
        self.construir_panel_superior()
        self.construir_area_graficos()
        
        # Dibujar los gráficos originales al abrir la ventana
        self.actualizar_graficos()

    def construir_panel_superior(self):
        panel = tk.Frame(self.ventana, bg="#ecf0f1", pady=10, padx=10)
        panel.pack(fill="x", side="top")
        
        tk.Label(panel, text="Transformar a Distribución:", bg="#ecf0f1", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        
        # Menú desplegable para elegir la distribución
        opciones = ["Uniforme (0, 1) - Original", "Uniforme (a, b)", "Exponencial", "Normal"]
        combo = ttk.Combobox(panel, textvariable=self.dist_actual, values=opciones, state="readonly", width=25)
        combo.pack(side="left", padx=5)
        combo.bind("<<ComboboxSelected>>", self.cambiar_inputs)
        
        # Contenedor donde aparecerán las cajas de texto (inputs) dinámicas
        self.frame_params = tk.Frame(panel, bg="#ecf0f1")
        self.frame_params.pack(side="left", padx=10)
        self.inputs_params = {}
        
        tk.Button(panel, text="Aplicar y Graficar 🔄", command=self.actualizar_graficos, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=10)

    def cambiar_inputs(self, event=None):
        """Muestra los campos correctos dependiendo de la distribución seleccionada."""
        for widget in self.frame_params.winfo_children():
            widget.destroy()
        self.inputs_params.clear()
        
        dist = self.dist_actual.get()
        
        if dist == "Exponencial":
            tk.Label(self.frame_params, text="Lambda (λ):", bg="#ecf0f1").pack(side="left")
            entry_lambda = tk.Entry(self.frame_params, width=10)
            entry_lambda.insert(0, "1.0")
            entry_lambda.pack(side="left", padx=5)
            self.inputs_params["lambda"] = entry_lambda
            
        elif dist == "Normal":
            tk.Label(self.frame_params, text="Media (μ):", bg="#ecf0f1").pack(side="left")
            entry_mu = tk.Entry(self.frame_params, width=10)
            entry_mu.insert(0, "0")
            entry_mu.pack(side="left", padx=5)
            self.inputs_params["mu"] = entry_mu
            
            tk.Label(self.frame_params, text="Desv. Est. (σ):", bg="#ecf0f1").pack(side="left")
            entry_sigma = tk.Entry(self.frame_params, width=10)
            entry_sigma.insert(0, "1")
            entry_sigma.pack(side="left", padx=5)
            self.inputs_params["sigma"] = entry_sigma
            
        elif dist == "Uniforme (a, b)":
            tk.Label(self.frame_params, text="Min (a):", bg="#ecf0f1").pack(side="left")
            entry_a = tk.Entry(self.frame_params, width=10)
            entry_a.insert(0, "10")
            entry_a.pack(side="left", padx=5)
            self.inputs_params["a"] = entry_a
            
            tk.Label(self.frame_params, text="Max (b):", bg="#ecf0f1").pack(side="left")
            entry_b = tk.Entry(self.frame_params, width=10)
            entry_b.insert(0, "20")
            entry_b.pack(side="left", padx=5)
            self.inputs_params["b"] = entry_b

    def construir_area_graficos(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.fig.patch.set_facecolor('#f5f6fa')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.ventana)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)

    def actualizar_graficos(self):
        dist = self.dist_actual.get()
        datos_transformados = self.datos_ri.copy()
        titulo_hist = "Histograma"
        
        try:
            # === TRANSFORMADAS INVERSAS ===
            if dist == "Exponencial":
                lam = float(self.inputs_params["lambda"].get())
                # Fórmula: X = (-1 / lambda) * ln(1 - Ri)
                # Sumamos 1e-10 para evitar un error matemático si Ri es exactamente 1
                datos_transformados = (-1 / lam) * np.log(1 - self.datos_ri + 1e-10)
                titulo_hist = f"Distribución Exponencial (λ={lam})"
                
            elif dist == "Normal":
                mu = float(self.inputs_params["mu"].get())
                sigma = float(self.inputs_params["sigma"].get())
                # Scipy tiene una función directa (ppf) para la transformada inversa de la normal
                datos_transformados = norm.ppf(self.datos_ri, loc=mu, scale=sigma)
                titulo_hist = f"Distribución Normal (μ={mu}, σ={sigma})"
                
            elif dist == "Uniforme (a, b)":
                a = float(self.inputs_params["a"].get())
                b = float(self.inputs_params["b"].get())
                # Fórmula: X = a + (b - a) * Ri
                datos_transformados = a + (b - a) * self.datos_ri
                titulo_hist = f"Distribución Uniforme Continua ({a}, {b})"
                
            else:
                titulo_hist = "Distribución Uniforme Original U(0,1)"

        except ValueError:
            messagebox.showerror("Error de Parámetros", "Asegúrate de ingresar solo números válidos.")
            return

        # Limpiar gráficos anteriores
        self.ax1.clear()
        self.ax2.clear()

        # Dibujar nuevo Histograma
        self.ax1.hist(datos_transformados, bins='auto', color='#8e44ad', edgecolor='black', alpha=0.7)
        self.ax1.set_title(titulo_hist, fontsize=11, fontweight='bold', color="#2c3e50")
        self.ax1.set_ylabel("Frecuencia")
        self.ax1.grid(True, linestyle='--', alpha=0.4)

        # Dibujar nueva Dispersión
        if len(datos_transformados) > 1:
            self.ax2.scatter(datos_transformados[:-1], datos_transformados[1:], color='#e67e22', alpha=0.6, s=15)
            self.ax2.set_title("Dispersión de los valores generados", fontsize=11, fontweight='bold', color="#2c3e50")
        self.ax2.grid(True, linestyle='--', alpha=0.4)
        
        self.fig.tight_layout()
        self.canvas.draw()

# Esta es la función que llama el main.py
def abrir_ventana_graficos(root_principal, datos):
    if not datos or len(datos) == 0:
        messagebox.showwarning("Sin datos", "Primero debes generar números pseudoaleatorios.")
        return
    VentanaGraficos(root_principal, datos)