import eel
import os
from scipy.integrate import odeint

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_web = os.path.join(directorio_actual, 'web')
eel.init(ruta_web)

estado = {
    "corriendo": False, "t": 0.0, "ovejas": 0.0, "lobos": 0.0,
    "alpha": 0.5, "beta": 0.02, "delta": 0.01, "gamma": 0.3, "dt": 0.1
}

def modelo_lotka_volterra(y0, t, alpha, beta, delta, gamma):
    return [
        alpha * y0[0] - beta * y0[0] * y0[1],
        delta * y0[0] * y0[1] - gamma * y0[1]
    ]

@eel.expose
def iniciar_simulacion(alpha, beta, delta, gamma, ovejas0, lobos0):
    estado.update({"alpha": alpha, "beta": beta, "delta": delta, "gamma": gamma, 
                   "ovejas": ovejas0, "lobos": lobos0, "t": 0.0, "corriendo": True})

@eel.expose
def detener_simulacion():
    estado["corriendo"] = False

@eel.expose
def reanudar_simulacion():
    estado["corriendo"] = True

@eel.expose
def actualizar_parametros(alpha, beta, delta, gamma):
    estado.update({"alpha": alpha, "beta": beta, "delta": delta, "gamma": gamma})


@eel.expose
def irAlInicio():
    import subprocess
    import os
    import sys

    print("Cerrando Lotka-Volterra y volviendo al menú...")

    # Carpeta donde está ESTE main.py (Lotka)
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

    # Carpeta del proyecto
    carpeta_proyecto = os.path.dirname(carpeta_actual)

    # main.py del menú principal
    ruta_main = os.path.join(carpeta_proyecto, "main.py")

    print("Ruta:", ruta_main)
    print("Existe:", os.path.exists(ruta_main))

    subprocess.Popen(
        [sys.executable, ruta_main],
        cwd=carpeta_actual
    )

    os._exit(0)

def loop_simulacion():
    while True:
        if estado["corriendo"]:
            y0 = [estado["ovejas"], estado["lobos"]]
            solucion = odeint(
                modelo_lotka_volterra, y0, [0, estado["dt"]], 
                args=(estado["alpha"], estado["beta"], estado["delta"], estado["gamma"])
            )
            
            estado["ovejas"] = max(0, solucion[1, 0])
            estado["lobos"] = max(0, solucion[1, 1])
            estado["t"] += estado["dt"]
            
            # Cálculo del punto de equilibrio matemático
            eq_ovejas = estado["gamma"] / estado["delta"] if estado["delta"] > 0 else 0
            eq_lobos = estado["alpha"] / estado["beta"] if estado["beta"] > 0 else 0
            
            try:
                eel.recibir_nuevo_punto(
                    estado["t"], estado["ovejas"], estado["lobos"], 
                    eq_ovejas, eq_lobos,
                    estado["alpha"], estado["beta"], estado["delta"], estado["gamma"]
                )()
            except Exception:
                pass
                
        eel.sleep(0.05)

if __name__ == '__main__':
    
    eel.spawn(loop_simulacion)
    try:
        eel.start('index.html', mode='edge', cmdline_args=['--start-maximized'], port=0)
    except EnvironmentError:
        eel.start('index.html', cmdline_args=['--start-maximized'], port=0)