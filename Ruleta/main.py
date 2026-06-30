import eel
import random
import time
import os

# Configuramos la ruta absoluta
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_web = os.path.join(directorio_actual, 'web')
eel.init(ruta_web)

# Variables globales de estado
saldo_inicial = 0
saldo_actual = 0
victorias = 0
derrotas = 0

@eel.expose
def iniciar_juego(saldo):
    """Guarda el saldo inicial ingresado por el usuario antes de jugar"""
    global saldo_inicial, saldo_actual, victorias, derrotas
    saldo_inicial = saldo
    saldo_actual = saldo
    victorias = 0
    derrotas = 0
    return saldo_actual

@eel.expose
def jugar_ruleta(apuesta, color_elegido):
    global saldo_actual, victorias, derrotas, saldo_inicial
    
    # Cobrar la apuesta
    saldo_actual -= apuesta
    
    # Girar ruleta
    numero_ganador = random.randint(0, 36)
    
    # Determinar color
    rojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    if numero_ganador == 0:
        color_ganador = "Verde"
    elif numero_ganador in rojos:
        color_ganador = "Rojo"
    else:
        color_ganador = "Negro"
        
    # Calcular si ganó o perdió
    ganancia = 0
    if color_elegido == color_ganador:
        ganancia = apuesta * 2
        saldo_actual += ganancia
        victorias += 1
    else:
        derrotas += 1
        
    # Calcular el saldo perdido o ganado neto
    beneficio_neto = saldo_actual - saldo_inicial 
        
    # Simular tiempo de la animación
    time.sleep(0.5)
    
    return {
        "numero": numero_ganador,
        "color": color_ganador,
        "saldo_actual": saldo_actual,
        "ganancia": ganancia,
        "victorias": victorias,
        "derrotas": derrotas,
        "beneficio_neto": beneficio_neto
    }

eel.start('index.html', mode='edge', size=(800, 750), port=0)