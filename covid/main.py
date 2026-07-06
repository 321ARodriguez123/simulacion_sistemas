import eel
import os
from game_logic import CovidSimulation

# Calculamos la cuadrícula base
COLS = 800 // 8
ROWS = 500 // 8

# Instancia global del juego
game = CovidSimulation(COLS, ROWS)
@eel.expose
def irInicio():
    import subprocess
    import os
    import sys

    print("Cerrando Covid y volviendo al menú...")

    # Carpeta donde está ESTE main.py (Covid)
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

@eel.expose
def get_initial_state():
    return game.get_state()

@eel.expose
def next_frame():
    game.update_generation()
    return game.get_state()

@eel.expose
def reset_simulation():
    global game
    game = CovidSimulation(COLS, ROWS)
    return game.get_state()

def main():
    # Le decimos a Eel que nuestros archivos web están en esta misma carpeta
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    eel.init(directorio_actual)
    
    print("Iniciando aplicación con Microsoft Edge...")
    
    # ¡Aquí está el cambio! Agregamos mode='edge'
    eel.start('index.html', mode='edge', size=(900, 850))

if __name__ == "__main__":
    main()