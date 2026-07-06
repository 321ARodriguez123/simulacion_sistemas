import numpy as np
from scipy.stats import norm, gamma, weibull_min, erlang

def obtener_datos_graficos(ri_list, distribucion, params):
    if not ri_list:
        raise ValueError("No hay datos para graficar.")
        
    ri_arr = np.array(ri_list)
    
    # === TRANSFORMACIONES ESTADÍSTICAS ===
    if distribucion == "Uniforme":
        # Extrae automáticamente el máximo y mínimo de los datos generados
        transformados = ri_arr
        min_ri = float(np.min(ri_arr))
        max_ri = float(np.max(ri_arr))
        titulo = f"Uniforme (Min={min_ri:.4f}, Max={max_ri:.4f})"
        
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
        transformados = gamma.ppf(ri_arr, a=alfa, scale=beta)
        titulo = f"Gamma (α={alfa}, β={beta})"
        
    elif distribucion == "k-Erlang":
        k = int(params.get('k', 2))
        lam_erlang = float(params.get('lam_erlang', 1.0))
        transformados = erlang.ppf(ri_arr, a=k, scale=1/lam_erlang)
        titulo = f"k-Erlang (k={k}, λ={lam_erlang})"
        
    elif distribucion == "Weibull":
        k_w = float(params.get('k_w', 1.5)) 
        lam_w = float(params.get('lam_w', 1.0)) 
        transformados = weibull_min.ppf(ri_arr, c=k_w, scale=lam_w)
        titulo = f"Weibull (k={k_w}, λ={lam_w})"
        
    else:
        transformados = ri_arr
        titulo = "Original U(0,1)"

    # Limpieza de valores matemáticamente inválidos (infinitos o NaN)
    transformados = np.nan_to_num(transformados, nan=0.0, posinf=0.0, neginf=0.0)

    # Agrupación para el histograma
    num_rangos = int(params.get('rangos', 10)) # 10 será el valor por defecto si falla
    counts, bin_edges = np.histogram(transformados, bins=num_rangos)
    hist_labels = [f"[{bin_edges[i]:.2f}, {bin_edges[i+1]:.2f}]" for i in range(len(counts))]
    hist_data = counts.tolist()
    
    # Puntos para el gráfico de dispersión
    scatter_data = [{"x": float(transformados[i]), "y": float(transformados[i+1])} for i in range(len(transformados)-1)] if len(transformados) > 1 else []

    return {
        "titulo": titulo,
        "hist_labels": hist_labels,
        "hist_data": hist_data,
        "scatter_data": scatter_data
    }