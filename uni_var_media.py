import numpy as np
from scipy.stats import chisquare, norm

def evaluar_media(datos, alpha=0.05):
    n = len(datos)
    media_calculada = np.mean(datos)
    z = abs(norm.ppf(alpha / 2))
    tolerancia = z * np.sqrt((1/12) / n) 
    es_valida = abs(media_calculada - 0.5) <= tolerancia
    return es_valida, media_calculada, tolerancia

def evaluar_varianza(datos, tolerancia=0.01):
    varianza_calculada = np.var(datos, ddof=1) if len(datos) > 1 else 0
    varianza_esperada = 1 / 12
    es_valida = abs(varianza_calculada - varianza_esperada) <= tolerancia
    return es_valida, varianza_calculada, varianza_esperada

def evaluar_uniformidad(datos, num_clases=10, alpha=0.05):
    n = len(datos)
    frecuencias_observadas, _ = np.histogram(datos, bins=num_clases, range=(0, 1))
    frecuencias_esperadas = [n / num_clases] * num_clases
    _, p_valor = chisquare(f_obs=frecuencias_observadas, f_exp=frecuencias_esperadas)
    es_valida = p_valor > alpha
    return es_valida, p_valor

def reporte_simulacion(datos, alpha=0.05):
    n = len(datos)
    if n == 0: return "Error: La lista de datos está vacía."

    media_ok, media_calc, tol_media = evaluar_media(datos, alpha)
    var_ok, var_calc, var_esp = evaluar_varianza(datos)
    unif_ok, p_valor = evaluar_uniformidad(datos, num_clases=10, alpha=alpha)

    # Construimos el texto del reporte para la interfaz
    rep = f"--- REPORTE (N={n}) ---\n\n"
    rep += f"1. Media: {media_calc:.4f} (Tol: ±{tol_media:.4f})\n   {'✅ PASÓ' if media_ok else '❌ FALLÓ'}\n\n"
    rep += f"2. Varianza: {var_calc:.4f} (Esp: {var_esp:.4f})\n   {'✅ PASÓ' if var_ok else '❌ FALLÓ'}\n\n"
    rep += f"3. Uniformidad p-valor: {p_valor:.4f}\n   {'✅ PASÓ' if unif_ok else '❌ FALLÓ'}\n\n"
    rep += "🟢 EXCELENTE" if (media_ok and var_ok and unif_ok) else "🔴 DEFICIENTE"
    
    return rep