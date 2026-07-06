import eel
import random
import time
import os
import numpy as np
from scipy.stats import norm, gamma, weibull_min, erlang

# Importamos tu lógica de simulación
import cuadrados_medios
import productos_medios
import multiplicador_contacto
import otro
import uni_var_media

# Inicializamos la carpeta del frontend usando la ruta absoluta
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_web = os.path.join(directorio_actual, 'web')
eel.init(ruta_web)

@eel.expose
def generar_simulacion(metodo, params):
    filas = []
    ri_list = []
    
    try:
        rango = int(params.get('rango', 10))
        
        if metodo == "Cuadrados Medios":
            filas, ri_list = cuadrados_medios.generar(int(params['semilla']), rango)
        elif metodo == "Productos Medios":
            filas, ri_list = productos_medios.generar(int(params['semilla1']), int(params['semilla2']), rango)
        elif metodo == "Multiplicador Constante":
            filas, ri_list = multiplicador_contacto.generar(int(params['a']), int(params['semilla']), rango)
        elif metodo == "Congruencial Lineal":
            filas, ri_list = otro.generar(int(params['a']), int(params['c']), int(params['semilla']), int(params['m']), rango)

        # Generamos los datos estructurados en lugar de texto
        stats = None
        if ri_list:
            m_ok, m_calc, m_tol = uni_var_media.evaluar_media(ri_list)
            v_ok, v_calc, v_esp = uni_var_media.evaluar_varianza(ri_list)
            u_ok, p_val = uni_var_media.evaluar_uniformidad(ri_list)
            
            # PYTHON HACE TODA LA LÓGICA Y FORMATEO
            stats = {
                "media": {
                    "val": f"{m_calc:.4f}", 
                    "tol": f"{m_tol:.4f}", 
                    "texto": "✅ PASO" if m_ok else "❌ FALLO",
                    "clase": "status-pass" if m_ok else "status-fail"
                },
                "varianza": {
                    "val": f"{v_calc:.4f}", 
                    "esp": f"{v_esp:.4f}", 
                    "texto": "✅ PASÓ" if v_ok else "❌ FALLÓ",
                    "clase": "status-pass" if v_ok else "status-fail"
                },
                "uniformidad": {
                    "p": f"{p_val:.4f}", 
                    "texto": "✅ PASÓ" if u_ok else "❌ FALLÓ",
                    "clase": "status-pass" if u_ok else "status-fail"
                }
            }
        
        return {"status": "success", "filas": filas, "ri_list": ri_list, "stats": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def procesar_graficos(ri_list, distribucion, params):
    if not ri_list:
        return {"status": "error", "message": "No hay datos para graficar."}
        
    try:
        ri_arr = np.array(ri_list)
        
        # === TRANSFORMACIONES ESTADÍSTICAS ===
        if distribucion == "Uniforme":
            a = float(params.get('a', 0))
            b = float(params.get('b', 1))
            transformados = a + (b - a) * ri_arr
            titulo = f"Uniforme (a={a}, b={b})"
            
        elif distribucion == "Exponencial":
            lam = float(params.get('lambda', 1.0))
            transformados = (-1 / lam) * np.log(1 - ri_arr + 1e-10)
            titulo = f"Exponencial (λ={lam})"
            
        elif distribucion == "Normal":
            mu = float(params.get('mu', 0))
            sigma = float(params.get('sigma', 1))
            transformados = norm.ppf(ri_arr, loc=mu, scale=sigma)
            titulo = f"Normal (μ={mu}, σ={sigma})"
            
        elif distribucion == "Gamma":
            alfa = float(params.get('alfa', 2.0))
            beta = float(params.get('beta', 1.0))
            # scipy usa 'a' para forma (alfa) y 'scale' para escala (beta)
            transformados = gamma.ppf(ri_arr, a=alfa, scale=beta)
            titulo = f"Gamma (α={alfa}, β={beta})"
            
        elif distribucion == "k-Erlang":
            k = int(params.get('k', 2))
            lam_erlang = float(params.get('lam_erlang', 1.0))
            # Erlang es un caso especial de Gamma donde k es entero
            transformados = erlang.ppf(ri_arr, a=k, scale=1/lam_erlang)
            titulo = f"k-Erlang (k={k}, λ={lam_erlang})"
            
        elif distribucion == "Weibull":
            k_w = float(params.get('k_w', 1.5)) # Forma
            lam_w = float(params.get('lam_w', 1.0)) # Escala
            transformados = weibull_min.ppf(ri_arr, c=k_w, scale=lam_w)
            titulo = f"Weibull (k={k_w}, λ={lam_w})"
            
        else:
            transformados = ri_arr
            titulo = "Original U(0,1)"

        # Asegurarnos de limpiar valores inválidos por límites matemáticos (inf/nan)
        transformados = np.nan_to_num(transformados, nan=0.0, posinf=0.0, neginf=0.0)

        # === AGRUPACIÓN PARA HISTOGRAMA (Estilo Excel) ===
        counts, bin_edges = np.histogram(transformados, bins='auto')
        
        # Formatear etiquetas de X como rangos matemáticos [min, max] idéntico a Excel
        hist_labels = [f"[{bin_edges[i]:.2f}, {bin_edges[i+1]:.2f}]" for i in range(len(counts))]
        hist_data = counts.tolist()

        # Datos para Dispersión
        scatter_data = [{"x": float(transformados[i]), "y": float(transformados[i+1])} for i in range(len(transformados)-1)] if len(transformados) > 1 else []

        return {
            "status": "success",
            "titulo": titulo,
            "hist_labels": hist_labels,
            "hist_data": hist_data,
            "scatter_data": scatter_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

if __name__ == '__main__':
    # Lanzamos la aplicación Eel en una ventana de Chrome/Edge
    eel.start('index.html', mode='edge', size=(1200, 800), position=(100, 50))