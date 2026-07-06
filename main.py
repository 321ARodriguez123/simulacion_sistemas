import eel
import random
import time
import os

# 1. Inicializar la carpeta web (le dice a Eel dónde buscar los archivos HTML/JS/CSS)
eel.init('web')
# 1. RUTA Y CONFIGURACIÓN (Solo una vez)
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_web = os.path.join(directorio_actual, 'web')
eel.init(ruta_web)


# 1. LotkaVoltera
@eel.expose
def irLotkaVoltera():
    import subprocess
    import os
    import sys

    print("Cerrando Menu y redirigiendo al Simulador Lotka-Volterra...")

    # Carpeta donde está ESTE main.py (Lotka)
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

    # main.py del menú principal
    ruta_lotka = os.path.join(carpeta_actual, "Lotka", "main.py")

    print("Ruta:", ruta_lotka)
    print("Existe:", os.path.exists(ruta_lotka))

    subprocess.Popen(
        [sys.executable, ruta_lotka],
        cwd=carpeta_actual
    )

    os._exit(0)


# 2. Covid
@eel.expose
def irCovid():
    import subprocess
    import os
    import sys

    print("Cerrando Menu y redirigiendo a Simulador Covid...")

    # Carpeta donde está ESTE main.py (Ruleta)
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

    # main.py del menú principal
    ruta_main = os.path.join(carpeta_actual, "covid", "main.py")

    print("Ruta:", ruta_main)
    print("Existe:", os.path.exists(ruta_main))

    subprocess.Popen(
        [sys.executable, ruta_main],
        cwd=carpeta_actual
    )

    os._exit(0)



# 3. Casino
@eel.expose
def irCasino():
    import subprocess
    import os
    import sys

    print("Cerrando Menu y redirigiendo a Simulador Covid...")

    # Carpeta donde está ESTE main.py (Ruleta)
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))


    # main.py del menú principal
    ruta_main = os.path.join(carpeta_actual, "Ruleta", "main.py")

    print("Ruta:", ruta_main)
    print("Existe:", os.path.exists(ruta_main))

    subprocess.Popen(
        [sys.executable, ruta_main],
        cwd=carpeta_actual
    )

    os._exit(0)


# 4. Calculadora
@eel.expose
def irCalculadora():
    import subprocess
    import os
    import sys

    print("Cerrando Menu y redirigiendo a Calculadora Covid...")

    # Carpeta donde está ESTE main.py (Calculadora)
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))


    # main.py del menú principal
    ruta_main = os.path.join(carpeta_actual, "Calculadora", "main.py")

    print("Ruta:", ruta_main)
    print("Existe:", os.path.exists(ruta_main))

    subprocess.Popen(
        [sys.executable, ruta_main],
        cwd=carpeta_actual
    )

    os._exit(0)


# 2. Exponer funciones de Python a JavaScript (Opcional)
# Tu HTML ya tiene toda la lógica, pero si quisieras usar Python para 
# generar el resultado de la ruleta, podrías usar una función como esta:
@eel.expose
def obtener_numero_ruleta_desde_python():
    """Ejemplo de cómo usar random y time en el backend"""
    # Simulamos un pequeño retraso de procesamiento usando 'time'
    time.sleep(0.5) 
    
    # Usamos 'random' para elegir un número de la ruleta europea
    numeros_ruleta = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 
                      30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 
                      29, 7, 28, 12, 35, 3, 26]
    
    resultado = random.choice(numeros_ruleta)
    print(f"[Python Backend] El servidor ha generado el número: {resultado}")
    return resultado



# 3. Iniciar la aplicación
if __name__ == '__main__':
    # Usamos 'os' para verificar en qué directorio estamos trabajando (solo por demostración)
    directorio_actual = os.getcwd()
    print(f"Iniciando el Portal de Simuladores desde: {directorio_actual}")
    
    # Inicia la ventana de la app. Busca 'index.html' dentro de la carpeta 'web'
    # Puedes ajustar el tamaño de la ventana con 'size'
    try:
        eel.start('index.html', mode='edge', size=(800, 750), port=0)

    except Exception as e:
        print(f"Error al iniciar Eel: {e}")
        # Como plan de respaldo por si el usuario no tiene Chrome instalado:
        eel.start('index.html', mode='edge', size=(800, 750), port=0)
