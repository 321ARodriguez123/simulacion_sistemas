import eel
import os
import numpy as np

# Importamos tu lógica de simulación
import cuadrados_medios
import productos_medios
import multiplicador_contacto
import otro
import uni_var_media
import graficos  # <--- Importamos tu archivo de gráficos actualizado

# Inicializamos la carpeta del frontend
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

        stats = None
        if ri_list:
            m_ok, m_calc, m_tol = uni_var_media.evaluar_media(ri_list)
            v_ok, v_calc, v_esp = uni_var_media.evaluar_varianza(ri_list)
            u_ok, p_val = uni_var_media.evaluar_uniformidad(ri_list)
            
            min_ri = float(np.min(ri_list))
            max_ri = float(np.max(ri_list))
            
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
                },
                "min_ri": f"{min_ri:.4f}",
                "max_ri": f"{max_ri:.4f}"
            }
        
        return {"status": "success", "filas": filas, "ri_list": ri_list, "stats": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def procesar_graficos(ri_list, distribucion, params):
    try:
        # Llamamos directamente a la lógica que modularizaste en graficos.py
        datos_grafico = graficos.obtener_datos_graficos(ri_list, distribucion, params)
        datos_grafico["status"] = "success"
        return datos_grafico
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    eel.start('index.html', mode='edge', size=(1200, 800), position=(100, 50))