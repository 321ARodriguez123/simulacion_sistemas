import numpy as np
from scipy.stats import chisquare, norm

# ==========================================
# 1. Función para evaluar la Media
# ==========================================
def evaluar_media(datos, alpha=0.05):
    """
    Verifica si la media de los datos tiende a 0.5 usando un intervalo de confianza.
    """
    n = len(datos)
    media_calculada = np.mean(datos)
    media_esperada = 0.5
    
    # Calculamos el valor Z para el nivel de confianza (ej. Z = 1.96 para alpha 0.05)
    z = abs(norm.ppf(alpha / 2))
    tolerancia = z * np.sqrt((1/12) / n) 
    
    es_valida = abs(media_calculada - media_esperada) <= tolerancia
    return es_valida, media_calculada, tolerancia

# ==========================================
# 2. Función para evaluar la Varianza
# ==========================================
def evaluar_varianza(datos, tolerancia=0.01):
    """
    Verifica si la varianza de los datos tiende a 1/12 (aprox 0.0833).
    """
    varianza_calculada = np.var(datos, ddof=1)
    varianza_esperada = 1 / 12
    
    es_valida = abs(varianza_calculada - varianza_esperada) <= tolerancia
    return es_valida, varianza_calculada, varianza_esperada

# ==========================================
# 3. Función para evaluar la Uniformidad
# ==========================================
def evaluar_uniformidad(datos, num_clases=10, alpha=0.05):
    """
    Aplica la prueba de Chi-cuadrado para comprobar si los números se
    distribuyen uniformemente entre 0 y 1.
    """
    n = len(datos)
    frecuencias_observadas, _ = np.histogram(datos, bins=num_clases, range=(0, 1))
    frecuencias_esperadas = [n / num_clases] * num_clases

    estadistico_chi, p_valor = chisquare(f_obs=frecuencias_observadas, f_exp=frecuencias_esperadas)
    
    # Si p_valor es mayor que alpha, no hay evidencia para rechazar la uniformidad
    es_valida = p_valor > alpha
    return es_valida, p_valor

# ==========================================
# Función Principal (Orquestador)
# ==========================================
def reporte_simulacion(datos, alpha=0.05):
    """
    Ejecuta las tres pruebas y genera un reporte completo de la simulación.
    """
    n = len(datos)
    if n == 0:
        return "Error: La lista de datos está vacía."

    # Ejecutamos nuestras funciones modulares
    media_ok, media_calc, tol_media = evaluar_media(datos, alpha)
    var_ok, var_calc, var_esp = evaluar_varianza(datos)
    unif_ok, p_valor = evaluar_uniformidad(datos, num_clases=10, alpha=alpha)

    # Imprimimos el reporte
    print(f"--- REPORTE DE SIMULACIÓN (N={n}) ---")
    
    print(f"1. Prueba de Media:")
    print(f"   - Valor: {media_calc:.4f} (Esperado: 0.5, Tolerancia: ±{tol_media:.4f})")
    print(f"   - Estado: {'✅ PASÓ' if media_ok else '❌ FALLÓ'}")
    
    print(f"2. Prueba de Varianza:")
    print(f"   - Valor: {var_calc:.4f} (Esperado: {var_esp:.4f})")
    print(f"   - Estado: {'✅ PASÓ' if var_ok else '❌ FALLÓ'}")
    
    print(f"3. Prueba de Uniformidad (Chi-cuadrado):")
    print(f"   - p-valor: {p_valor:.4f} (Umbral > {alpha})")
    print(f"   - Estado: {'✅ PASÓ' if unif_ok else '❌ FALLÓ'}")
    
    print("-" * 37)

    # Veredicto final
    if media_ok and var_ok and unif_ok:
        return "VEREDICTO: 🟢 SIMULACIÓN EXCELENTE.\n"
    else:
        return "VEREDICTO: 🔴 SIMULACIÓN DEFICIENTE. Revisa tu algoritmo generador.\n"

# ==========================================
# Ejemplos de uso
# ==========================================
if __name__ == "__main__":
    print(">>> PROBANDO DATOS CORRECTOS <<<")
    datos_buenos = np.random.uniform(0, 1, 5000)
    print(reporte_simulacion(datos_buenos))

    print(">>> PROBANDO DATOS CON SESGO (MALOS) <<<")
    # Generamos números entre 0.2 y 0.8 (fallará la varianza y uniformidad)
    datos_sesgados = np.random.uniform(0.2, 0.8, 5000)
    print(reporte_simulacion(datos_sesgados))