"""
================================================================================
 RULETA DE CASINO - Juego completo en Python con Pygame
================================================================================
Descripción:
    Simulación de una ruleta de casino europea (37 números: 0 al 36) con:
      - Rueda animada (giro con desaceleración realista) a la izquierda.
      - Tablero de apuestas clásico a la derecha (números, color, par/impar,
        docenas, columnas).
      - Selector de ficha, saldo en tiempo real y panel de historial.

Requisitos:
    pip install pygame

Ejecución:
    python ruleta_casino.py

Controles:
    - Click izquierdo sobre el tablero -> coloca una ficha (apuesta).
    - Click sobre los botones de ficha ($5/$10/$25/$50/$100) -> cambia el
      valor de la ficha que se está apostando.
    - Botón "GIRAR"             -> lanza la animación de la ruleta.
    - Botón "LIMPIAR APUESTAS"  -> retira todas las apuestas (antes de girar).
    - Botón "GUARDAR RESULTADO" -> guarda la última ronda jugada en
      historial_ruleta.json y la muestra en el panel de historial.
================================================================================
"""

import pygame
import random
import json
import math
import os
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN GENERAL Y CONSTANTES
# ==============================================================================
pygame.init()
pygame.font.init()

ANCHO_VENTANA = 1280
ALTO_VENTANA = 760
FPS = 60

# --- Paleta de colores ---
BLANCO = (245, 245, 245)
NEGRO = (18, 18, 18)
GRIS_OSCURO = (40, 40, 40)
GRIS = (70, 70, 70)
GRIS_CLARO = (160, 160, 160)
ROJO = (178, 34, 34)
ROJO_CLARO = (210, 60, 60)
VERDE_MESA = (10, 90, 55)
VERDE_OSCURO = (6, 60, 38)
DORADO = (212, 175, 55)
AMARILLO = (235, 200, 40)
AZUL = (40, 100, 180)
VERDE_OK = (60, 170, 90)
ROJO_ERROR = (200, 70, 70)

# Números rojos en una ruleta europea estándar (el resto, excepto el 0, son negros)
NUMEROS_ROJOS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

# Orden físico de los números alrededor de la rueda europea (37 casilleros)
ORDEN_RUEDA = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
               5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# Pagos (a 1) por tipo de apuesta. El jugador recupera además su ficha original.
PAGOS = {
    "pleno": 35,
    "rojo": 1, "negro": 1,
    "par": 1, "impar": 1,
    "1-18": 1, "19-36": 1,
    "docena1": 2, "docena2": 2, "docena3": 2,
    "columna1": 2, "columna2": 2, "columna3": 2,
}

# Etiquetas legibles para mostrar en el historial
ETIQUETAS = {
    "rojo": "Rojo", "negro": "Negro", "par": "Par", "impar": "Impar",
    "1-18": "1-18", "19-36": "19-36",
    "docena1": "1ra Docena", "docena2": "2da Docena", "docena3": "3ra Docena",
    "columna1": "Columna 1", "columna2": "Columna 2", "columna3": "Columna 3",
}

ARCHIVO_HISTORIAL = "historial_ruleta.json"
SALDO_INICIAL = 1000
VALORES_FICHA = [5, 10, 25, 50, 100]

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ruleta de Casino - Python / Pygame")
reloj = pygame.time.Clock()

fuente_mini = pygame.font.SysFont("arial", 13)
fuente_chica = pygame.font.SysFont("arial", 15)
fuente_normal = pygame.font.SysFont("arial", 18, bold=True)
fuente_grande = pygame.font.SysFont("arial", 30, bold=True)
fuente_titulo = pygame.font.SysFont("arial", 24, bold=True)


def color_de_numero(n):
    """Devuelve el color real (rojo/negro/verde) de un número de la ruleta."""
    if n == 0:
        return VERDE_MESA
    return ROJO if n in NUMEROS_ROJOS else NEGRO


def gana_apuesta(tipo, valor, numero_ganador):
    """Determina si una apuesta (tipo, valor) gana dado el número ganador."""
    if tipo == "pleno":
        return valor == numero_ganador
    if numero_ganador == 0:
        # El 0 sólo puede ganarse con apuesta "pleno" al 0
        return False
    if tipo == "rojo":
        return numero_ganador in NUMEROS_ROJOS
    if tipo == "negro":
        return numero_ganador not in NUMEROS_ROJOS
    if tipo == "par":
        return numero_ganador % 2 == 0
    if tipo == "impar":
        return numero_ganador % 2 == 1
    if tipo == "1-18":
        return 1 <= numero_ganador <= 18
    if tipo == "19-36":
        return 19 <= numero_ganador <= 36
    if tipo == "docena1":
        return 1 <= numero_ganador <= 12
    if tipo == "docena2":
        return 13 <= numero_ganador <= 24
    if tipo == "docena3":
        return 25 <= numero_ganador <= 36
    if tipo == "columna1":
        return numero_ganador % 3 == 1
    if tipo == "columna2":
        return numero_ganador % 3 == 2
    if tipo == "columna3":
        return numero_ganador % 3 == 0
    return False


# ==============================================================================
# 2. COMPONENTE: BOTÓN GENÉRICO
# ==============================================================================
class Boton:
    """Botón rectangular simple, reutilizable para toda la interfaz."""

    def __init__(self, rect, texto, color_fondo, color_texto=BLANCO, fuente=None,
                 borde_color=None):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.fuente = fuente or fuente_normal
        self.borde_color = borde_color
        self.activo = True  # si False, se dibuja "deshabilitado" y no responde

    def dibujar(self, superficie, resaltado=False):
        color = self.color_fondo if self.activo else GRIS
        if resaltado and self.activo:
            color = tuple(min(255, c + 35) for c in color)
        pygame.draw.rect(superficie, color, self.rect, border_radius=8)
        borde = self.borde_color if self.borde_color else NEGRO
        pygame.draw.rect(superficie, borde, self.rect, width=2, border_radius=8)
        texto_render = self.fuente.render(self.texto, True, self.color_texto)
        x = self.rect.centerx - texto_render.get_width() // 2
        y = self.rect.centery - texto_render.get_height() // 2
        superficie.blit(texto_render, (x, y))

    def clic_dentro(self, pos):
        return self.activo and self.rect.collidepoint(pos)


# ==============================================================================
# 3. COMPONENTE: RUEDA DE LA RULETA (con animación)
# ==============================================================================
class Ruleta:
    """Representa la rueda física: su dibujo y la animación de giro."""

    def __init__(self, centro, radio):
        self.centro = centro
        self.radio = radio
        self.angulo = 0.0
        self.girando = False
        self.angulo_inicial = 0.0
        self.angulo_objetivo = 0.0
        self.tiempo_inicio = 0
        self.duracion_giro = 3800  # milisegundos que dura la animación
        self.numero_ganador = None
        self.callback_fin = None

    def iniciar_giro(self, numero_ganador, callback_fin=None):
        """Lanza la animación calculando el ángulo final para que el número
        ganador termine exactamente bajo el indicador (flecha superior)."""
        self.numero_ganador = numero_ganador
        self.callback_fin = callback_fin

        n_casilleros = len(ORDEN_RUEDA)
        angulo_por_numero = 360 / n_casilleros
        indice = ORDEN_RUEDA.index(numero_ganador)
        angulo_numero = indice * angulo_por_numero + angulo_por_numero / 2

        vueltas_extra = random.randint(4, 7) * 360
        objetivo_base = (360 - angulo_numero) % 360

        self.angulo_inicial = self.angulo % 360
        objetivo = self.angulo_inicial + vueltas_extra + objetivo_base
        # Asegura que siempre rote "hacia adelante" una distancia positiva
        while objetivo <= self.angulo_inicial:
            objetivo += 360
        self.angulo_objetivo = objetivo

        self.tiempo_inicio = pygame.time.get_ticks()
        self.girando = True

    def actualizar(self):
        if not self.girando:
            return
        ahora = pygame.time.get_ticks()
        t = min((ahora - self.tiempo_inicio) / self.duracion_giro, 1.0)
        # Easing "ease-out cubic": empieza rápido y frena suavemente al final
        t_suavizado = 1 - (1 - t) ** 3
        self.angulo = self.angulo_inicial + (self.angulo_objetivo - self.angulo_inicial) * t_suavizado
        if t >= 1.0:
            self.girando = False
            self.angulo = self.angulo_objetivo % 360
            if self.callback_fin:
                self.callback_fin(self.numero_ganador)

    def dibujar(self, superficie):
        n = len(ORDEN_RUEDA)
        angulo_por_numero = 360 / n

        # Aro exterior decorativo
        pygame.draw.circle(superficie, DORADO, self.centro, self.radio + 14)
        pygame.draw.circle(superficie, NEGRO, self.centro, self.radio + 9)

        for i, numero in enumerate(ORDEN_RUEDA):
            a0 = math.radians(self.angulo + i * angulo_por_numero - 90)
            a1 = math.radians(self.angulo + (i + 1) * angulo_por_numero - 90)
            color = color_de_numero(numero)

            # Resalta con un brillo el sector ganador una vez que se detiene
            if (not self.girando) and self.numero_ganador == numero:
                color = tuple(min(255, c + 70) for c in color)

            puntos = [self.centro]
            pasos = 6
            for p in range(pasos + 1):
                ang = a0 + (a1 - a0) * p / pasos
                x = self.centro[0] + self.radio * math.cos(ang)
                y = self.centro[1] + self.radio * math.sin(ang)
                puntos.append((x, y))
            pygame.draw.polygon(superficie, color, puntos)
            pygame.draw.polygon(superficie, GRIS_OSCURO, puntos, width=1)

            ang_medio = (a0 + a1) / 2
            tx = self.centro[0] + (self.radio - 20) * math.cos(ang_medio)
            ty = self.centro[1] + (self.radio - 20) * math.sin(ang_medio)
            texto = fuente_mini.render(str(numero), True, BLANCO)
            superficie.blit(texto, (tx - texto.get_width() / 2, ty - texto.get_height() / 2))

        # Centro / eje de la rueda
        pygame.draw.circle(superficie, GRIS_CLARO, self.centro, int(self.radio * 0.32))
        pygame.draw.circle(superficie, NEGRO, self.centro, int(self.radio * 0.32), width=3)
        pygame.draw.circle(superficie, DORADO, self.centro, int(self.radio * 0.06))

        # Indicador fijo (flecha) que marca el número ganador en la parte superior
        px, py = self.centro[0], self.centro[1] - self.radio - 24
        pygame.draw.polygon(superficie, AMARILLO,
                             [(px - 13, py - 20), (px + 13, py - 20), (px, py + 8)])
        pygame.draw.polygon(superficie, NEGRO,
                             [(px - 13, py - 20), (px + 13, py - 20), (px, py + 8)], width=2)

        # Texto grande con el número ganador, debajo de la rueda, al detenerse
        if (not self.girando) and self.numero_ganador is not None:
            color_txt = color_de_numero(self.numero_ganador)
            etiqueta = fuente_grande.render(f"Número ganador: {self.numero_ganador}", True, AMARILLO)
            fondo = etiqueta.get_rect()
            fondo.center = (self.centro[0], self.centro[1] + self.radio + 38)
            pygame.draw.rect(superficie, color_txt, fondo.inflate(20, 10), border_radius=6)
            pygame.draw.rect(superficie, NEGRO, fondo.inflate(20, 10), width=2, border_radius=6)
            superficie.blit(etiqueta, fondo)


# ==============================================================================
# 4. COMPONENTE: TABLERO DE APUESTAS
# ==============================================================================
class Tablero:
    """Construye y dibuja el tapete de apuestas, y resuelve qué casilla
    corresponde a un clic del mouse."""

    def __init__(self, x, y):
        self.celdas = []  # cada celda: {"rect", "tipo", "valor", "etiqueta"}
        self._construir(x, y)

    def _construir(self, x, y):
        CELL_W, CELL_H = 46, 50

        # --- Casilla del 0 (a la izquierda de la grilla, abarca las 3 filas) ---
        zero_rect = pygame.Rect(x, y, CELL_W, CELL_H * 3)
        self.celdas.append({"rect": zero_rect, "tipo": "pleno", "valor": 0, "etiqueta": "0"})

        grid_x = x + CELL_W

        # --- Grilla principal 1-36 (3 filas x 12 columnas) ---
        # fila superior: 3,6,9...36 | fila media: 2,5,8...35 | fila inferior: 1,4,7...34
        for col in range(12):
            base = (col + 1) * 3
            for fila, numero in enumerate([base, base - 1, base - 2]):
                rect = pygame.Rect(grid_x + col * CELL_W, y + fila * CELL_H, CELL_W, CELL_H)
                self.celdas.append({"rect": rect, "tipo": "pleno", "valor": numero,
                                     "etiqueta": str(numero)})

        grid_ancho = CELL_W * 12
        borde_derecho = grid_x + grid_ancho

        # --- Apuestas de columna ("2 a 1"), a la derecha de cada fila ---
        col_bet_w = 64
        mapa_columnas = [("columna3", "2 a 1"), ("columna2", "2 a 1"), ("columna1", "2 a 1")]
        for fila, (tipo, etiqueta) in enumerate(mapa_columnas):
            rect = pygame.Rect(borde_derecho, y + fila * CELL_H, col_bet_w, CELL_H)
            self.celdas.append({"rect": rect, "tipo": tipo, "valor": None, "etiqueta": etiqueta})

        # --- Docenas (debajo de la grilla) ---
        y_docenas = y + CELL_H * 3
        docena_w = grid_ancho // 3
        docenas = [("docena1", "1ra 12"), ("docena2", "2da 12"), ("docena3", "3ra 12")]
        for i, (tipo, etiqueta) in enumerate(docenas):
            rect = pygame.Rect(grid_x + i * docena_w, y_docenas, docena_w, 42)
            self.celdas.append({"rect": rect, "tipo": tipo, "valor": None, "etiqueta": etiqueta})

        # --- Fila de apuestas simples (1-18, PAR, ROJO, NEGRO, IMPAR, 19-36) ---
        y_simples = y_docenas + 42
        simple_w = grid_ancho // 6
        simples = [("1-18", "1-18"), ("par", "PAR"), ("rojo", "ROJO"),
                   ("negro", "NEGRO"), ("impar", "IMPAR"), ("19-36", "19-36")]
        for i, (tipo, etiqueta) in enumerate(simples):
            rect = pygame.Rect(grid_x + i * simple_w, y_simples, simple_w, 42)
            self.celdas.append({"rect": rect, "tipo": tipo, "valor": None, "etiqueta": etiqueta})

        self.borde_total = pygame.Rect(x, y, (borde_derecho + col_bet_w) - x,
                                        (y_simples + 42) - y)

    def celda_en(self, pos):
        for celda in self.celdas:
            if celda["rect"].collidepoint(pos):
                return celda
        return None

    def dibujar(self, superficie, apuestas, numero_ganador=None, mostrar_resultado=False):
        pygame.draw.rect(superficie, VERDE_OSCURO, self.borde_total.inflate(10, 10), border_radius=10)

        for celda in self.celdas:
            rect = celda["rect"]
            tipo, valor = celda["tipo"], celda["valor"]

            # --- Color de fondo según el tipo de celda ---
            if tipo == "pleno":
                color = color_de_numero(valor)
            elif tipo == "rojo":
                color = ROJO
            elif tipo == "negro":
                color = NEGRO
            else:
                color = VERDE_MESA

            # Resalta la celda ganadora una vez resuelta la ronda
            ganadora = mostrar_resultado and numero_ganador is not None and \
                gana_apuesta(tipo, valor, numero_ganador)
            if ganadora:
                color = tuple(min(255, c + 90) for c in color)

            pygame.draw.rect(superficie, color, rect)
            pygame.draw.rect(superficie, DORADO if ganadora else GRIS_CLARO, rect, width=2)

            texto = fuente_chica.render(celda["etiqueta"], True, BLANCO)
            superficie.blit(texto, (rect.centerx - texto.get_width() / 2,
                                     rect.centery - texto.get_height() / 2))

        # --- Dibuja las fichas colocadas sobre cada celda apostada ---
        for (tipo, valor), monto in apuestas.items():
            celda = next((c for c in self.celdas if c["tipo"] == tipo and c["valor"] == valor), None)
            if celda is None:
                continue
            cx, cy = celda["rect"].center
            pygame.draw.circle(superficie, AMARILLO, (cx, cy), 14)
            pygame.draw.circle(superficie, NEGRO, (cx, cy), 14, width=2)
            texto_monto = fuente_mini.render(f"{monto}", True, NEGRO)
            superficie.blit(texto_monto, (cx - texto_monto.get_width() / 2,
                                           cy - texto_monto.get_height() / 2))


# ==============================================================================
# 5. CLASE PRINCIPAL DEL JUEGO
# ==============================================================================
class Juego:
    def __init__(self):
        self.saldo = SALDO_INICIAL
        self.ficha_valor = VALORES_FICHA[0]
        self.apuestas = {}          # {(tipo, valor): monto}
        self.numero_ganador = None
        self.girando_resuelto = False  # True cuando ya hay un resultado mostrado
        self.mensaje = "Coloca tus apuestas y presiona GIRAR"
        self.color_mensaje = BLANCO
        self.ultima_ronda = None    # dict con el detalle de la última ronda jugada
        self.historial = self._cargar_historial()

        # --- Construcción de componentes visuales ---
        self.ruleta = Ruleta(centro=(280, 225), radio=158)
        self.tablero = Tablero(x=626, y=60)

        self._construir_botones()

    # --------------------------------------------------------------------
    def _construir_botones(self):
        # Botones de selección de ficha
        self.botones_ficha = []
        x0 = 40
        for i, valor in enumerate(VALORES_FICHA):
            rect = (x0 + i * 75, 520, 65, 40)
            self.botones_ficha.append(Boton(rect, f"${valor}", GRIS, fuente=fuente_chica))

        # Botones de control principales
        self.boton_girar = Boton((40, 580, 160, 50), "GIRAR", VERDE_OK, fuente=fuente_normal)
        self.boton_limpiar = Boton((215, 580, 180, 50), "LIMPIAR APUESTAS", AZUL, fuente=fuente_chica)
        self.boton_guardar = Boton((40, 645, 355, 45), "GUARDAR RESULTADO", DORADO,
                                    color_texto=NEGRO, fuente=fuente_chica)

    # --------------------------------------------------------------------
    def _cargar_historial(self):
        if os.path.exists(ARCHIVO_HISTORIAL):
            try:
                with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _guardar_historial_en_disco(self):
        with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
            json.dump(self.historial, f, indent=2, ensure_ascii=False)

    # --------------------------------------------------------------------
    def total_apostado(self):
        return sum(self.apuestas.values())

    def manejar_clic(self, pos):
        # 1) Botones de selección de ficha (siempre disponibles)
        for boton, valor in zip(self.botones_ficha, VALORES_FICHA):
            if boton.clic_dentro(pos):
                self.ficha_valor = valor
                return

        # 2) Botón GIRAR
        if self.boton_girar.clic_dentro(pos):
            self._intentar_girar()
            return

        # 3) Botón LIMPIAR APUESTAS (sólo si la rueda no está girando)
        if self.boton_limpiar.clic_dentro(pos) and not self.ruleta.girando:
            self.apuestas = {}
            self.mensaje = "Apuestas retiradas."
            self.color_mensaje = BLANCO
            return

        # 4) Botón GUARDAR RESULTADO
        if self.boton_guardar.clic_dentro(pos):
            self._guardar_resultado()
            return

        # 5) Clic sobre el tablero -> colocar ficha (sólo si no está girando
        #    y no hay un resultado pendiente de limpiar)
        if not self.ruleta.girando and not self.girando_resuelto:
            celda = self.tablero.celda_en(pos)
            if celda:
                self._colocar_ficha(celda)

    def _colocar_ficha(self, celda):
        if self.ficha_valor > self.saldo - self.total_apostado():
            self.mensaje = "Saldo insuficiente para esa ficha."
            self.color_mensaje = ROJO_ERROR
            return
        clave = (celda["tipo"], celda["valor"])
        self.apuestas[clave] = self.apuestas.get(clave, 0) + self.ficha_valor
        self.mensaje = f"Apuesta colocada: {celda['etiqueta']} (${self.ficha_valor})"
        self.color_mensaje = BLANCO

    # --------------------------------------------------------------------
    def _intentar_girar(self):
        if self.ruleta.girando:
            return
        if self.total_apostado() == 0:
            self.mensaje = "Debes colocar al menos una apuesta."
            self.color_mensaje = ROJO_ERROR
            return
        if self.total_apostado() > self.saldo:
            self.mensaje = "El total apostado supera tu saldo."
            self.color_mensaje = ROJO_ERROR
            return

        # Se descuenta el total apostado del saldo (se "pone en juego")
        self.saldo -= self.total_apostado()
        self.girando_resuelto = False
        self.numero_ganador = None
        self.ruleta.numero_ganador = None
        self.mensaje = "¡Girando la ruleta...!"
        self.color_mensaje = AMARILLO

        numero_ganador = random.randint(0, 36)
        self.ruleta.iniciar_giro(numero_ganador, callback_fin=self._resolver_ronda)

    def _resolver_ronda(self, numero_ganador):
        """Se ejecuta automáticamente cuando la animación de la rueda termina."""
        self.numero_ganador = numero_ganador
        total_apostado = self.total_apostado()
        ganancia_total = 0
        detalle_apuestas = []

        for (tipo, valor), monto in self.apuestas.items():
            etiqueta = str(valor) if tipo == "pleno" else ETIQUETAS.get(tipo, tipo)
            gano = gana_apuesta(tipo, valor, numero_ganador)
            if gano:
                pago = PAGOS[tipo]
                retorno = monto * (pago + 1)  # ficha original + ganancia
                ganancia_total += retorno
            detalle_apuestas.append({"apuesta": etiqueta, "monto": monto, "gano": gano})

        self.saldo += ganancia_total
        balance_neto = ganancia_total - total_apostado

        if balance_neto > 0:
            self.mensaje = f"¡Ganaste ${balance_neto}! Número: {numero_ganador}"
            self.color_mensaje = VERDE_OK
        elif balance_neto < 0:
            self.mensaje = f"Perdiste ${abs(balance_neto)}. Número: {numero_ganador}"
            self.color_mensaje = ROJO_ERROR
        else:
            self.mensaje = f"Empate (recuperaste tu apuesta). Número: {numero_ganador}"
            self.color_mensaje = BLANCO

        self.ultima_ronda = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_apostado": total_apostado,
            "apuestas": detalle_apuestas,
            "numero_ganador": numero_ganador,
            "balance_neto": balance_neto,
            "saldo_resultante": self.saldo,
        }
        self.girando_resuelto = True

    def _guardar_resultado(self):
        if self.ultima_ronda is None:
            self.mensaje = "No hay ninguna ronda jugada para guardar todavía."
            self.color_mensaje = ROJO_ERROR
            return
        self.historial.append(self.ultima_ronda)
        self._guardar_historial_en_disco()
        self.mensaje = "Resultado guardado en el historial."
        self.color_mensaje = VERDE_OK
        # Se limpia el tablero para iniciar una nueva ronda
        self.apuestas = {}
        self.ultima_ronda = None
        self.girando_resuelto = False
        self.ruleta.numero_ganador = None

    # --------------------------------------------------------------------
    def actualizar(self):
        self.ruleta.actualizar()

    # --------------------------------------------------------------------
    def dibujar(self, superficie):
        superficie.fill(VERDE_OSCURO)

        # --- Panel izquierdo: rueda + controles ---
        self.ruleta.dibujar(superficie)

        # Saldo y apuesta total
        texto_saldo = fuente_titulo.render(f"Saldo: ${self.saldo}", True, DORADO)
        superficie.blit(texto_saldo, (40, 470))
        texto_apostado = fuente_chica.render(f"Total apostado: ${self.total_apostado()}", True, BLANCO)
        superficie.blit(texto_apostado, (40, 500))

        # Selector de ficha
        for boton, valor in zip(self.botones_ficha, VALORES_FICHA):
            boton.dibujar(superficie, resaltado=(valor == self.ficha_valor))

        # Botones de control
        self.boton_girar.activo = not self.ruleta.girando
        self.boton_limpiar.activo = not self.ruleta.girando
        self.boton_girar.dibujar(superficie)
        self.boton_limpiar.dibujar(superficie)
        self.boton_guardar.dibujar(superficie)

        # Mensaje de estado
        texto_msg = fuente_chica.render(self.mensaje, True, self.color_mensaje)
        superficie.blit(texto_msg, (40, 700))

        # --- Panel derecho: tablero de apuestas ---
        titulo_tablero = fuente_titulo.render("TABLERO DE APUESTAS", True, DORADO)
        superficie.blit(titulo_tablero, (626, 25))
        self.tablero.dibujar(superficie, self.apuestas, self.numero_ganador,
                              mostrar_resultado=self.girando_resuelto)

        # --- Panel de historial (debajo del tablero) ---
        self._dibujar_historial(superficie, x=570, y=320, ancho=680, alto=400)

    def _dibujar_historial(self, superficie, x, y, ancho, alto):
        panel = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(superficie, GRIS_OSCURO, panel, border_radius=8)
        pygame.draw.rect(superficie, DORADO, panel, width=2, border_radius=8)

        titulo = fuente_normal.render("HISTORIAL DE RONDAS GUARDADAS", True, DORADO)
        superficie.blit(titulo, (x + 14, y + 10))

        fila_y = y + 42
        # Se muestran las últimas rondas guardadas, las más recientes primero
        ultimas = list(reversed(self.historial))[:9]
        if not ultimas:
            vacio = fuente_chica.render("Aún no se guardó ninguna ronda.", True, GRIS_CLARO)
            superficie.blit(vacio, (x + 14, fila_y))
            return

        for ronda in ultimas:
            color_balance = VERDE_OK if ronda["balance_neto"] > 0 else (
                ROJO_ERROR if ronda["balance_neto"] < 0 else BLANCO)
            signo = "+" if ronda["balance_neto"] >= 0 else ""
            linea = (f"{ronda['fecha'][:16]}  |  Apostado: ${ronda['total_apostado']}  |  "
                     f"Ganador: {ronda['numero_ganador']}  |  Neto: {signo}{ronda['balance_neto']}")
            texto = fuente_mini.render(linea, True, color_balance)
            superficie.blit(texto, (x + 14, fila_y))
            fila_y += 24
            if fila_y > y + alto - 24:
                break


# ==============================================================================
# 6. BUCLE PRINCIPAL
# ==============================================================================
def main():
    juego = Juego()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                juego.manejar_clic(evento.pos)

        juego.actualizar()
        juego.dibujar(ventana)
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
