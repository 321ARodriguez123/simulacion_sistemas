import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation


# ====================================================
# 1. Modelo tipo Lotka-Volterra aplicado a Bolivia
# ====================================================
def modelo_bolivia(y0, t, alpha, beta, delta, gamma):
    """
    y0[0] = disponibilidad de dólares
    y0[1] = presión económica/cambiaria

    Fórmula base:

    dx/dt = alpha*x - beta*x*y
    dy/dt = delta*x*y - gamma*y
    """

    dolares = y0[0]
    presion = y0[1]

    # Disponibilidad de dólares
    ddolares_dt = alpha * dolares - beta * dolares * presion

    # Presión económica/cambiaria
    dpresion_dt = delta * dolares * presion - gamma * presion

    return [ddolares_dt, dpresion_dt]


# ====================================================
# 2. Función para resolver el sistema
# ====================================================
def resolver_modelo(alpha, beta, delta, gamma, dolares0, presion0, tiempo_final):
    t = np.linspace(0, tiempo_final, 1000)
    y0 = [dolares0, presion0]

    solucion = odeint(
        modelo_bolivia,
        y0,
        t,
        args=(alpha, beta, delta, gamma)
    )

    return t, solucion


# ====================================================
# 3. Parámetros iniciales
# ====================================================
alpha0 = 0.25
beta0 = 0.08
delta0 = 0.04
gamma0 = 0.30

dolares0 = 10
presion0 = 4
tiempo_final0 = 60


# ====================================================
# 4. Primera simulación
# ====================================================
t, solucion = resolver_modelo(
    alpha0,
    beta0,
    delta0,
    gamma0,
    dolares0,
    presion0,
    tiempo_final0
)

dolares = solucion[:, 0]
presion = solucion[:, 1]


# ====================================================
# 5. Crear ventana de gráficos
# ====================================================
fig, axs = plt.subplots(1, 2, figsize=(15, 8))
plt.subplots_adjust(bottom=0.42)


# ----------------------------------------------------
# Gráfico 1: evolución en el tiempo
# ----------------------------------------------------
linea_dolares, = axs[0].plot(t, dolares, label="Disponibilidad de dólares")
linea_presion, = axs[0].plot(t, presion, label="Presión económica/cambiaria")

punto_dolares, = axs[0].plot(t[0], dolares[0], "o")
punto_presion, = axs[0].plot(t[0], presion[0], "o")

axs[0].set_title("Bolivia: dinámica en el tiempo")
axs[0].set_xlabel("Tiempo")
axs[0].set_ylabel("Índice")
axs[0].legend()
axs[0].grid(alpha=0.3)


# ----------------------------------------------------
# Gráfico 2: espacio de fase
# ----------------------------------------------------
linea_fase, = axs[1].plot(dolares, presion, label="Trayectoria")
punto_fase, = axs[1].plot(dolares[0], presion[0], "o", label="Estado actual")

equilibrio_x = gamma0 / delta0
equilibrio_y = alpha0 / beta0

punto_equilibrio = axs[1].scatter(
    equilibrio_x,
    equilibrio_y,
    s=100,
    label="Punto de equilibrio"
)

axs[1].set_title("Espacio de fase")
axs[1].set_xlabel("Disponibilidad de dólares")
axs[1].set_ylabel("Presión económica/cambiaria")
axs[1].legend()
axs[1].grid(alpha=0.3)


# ----------------------------------------------------
# Texto informativo
# ----------------------------------------------------
texto_info = fig.text(
    0.5,
    0.35,
    "",
    ha="center",
    fontsize=11
)


# ====================================================
# 6. Crear sliders
# ====================================================
ax_alpha = plt.axes([0.15, 0.28, 0.70, 0.025])
ax_beta = plt.axes([0.15, 0.24, 0.70, 0.025])
ax_delta = plt.axes([0.15, 0.20, 0.70, 0.025])
ax_gamma = plt.axes([0.15, 0.16, 0.70, 0.025])

ax_dolares0 = plt.axes([0.15, 0.12, 0.70, 0.025])
ax_presion0 = plt.axes([0.15, 0.08, 0.70, 0.025])
ax_tiempo = plt.axes([0.15, 0.04, 0.70, 0.025])


slider_alpha = Slider(
    ax_alpha,
    "alpha: entrada de dólares",
    0.01,
    1.0,
    valinit=alpha0,
    valstep=0.01
)

slider_beta = Slider(
    ax_beta,
    "beta: presión sobre dólares",
    0.01,
    0.5,
    valinit=beta0,
    valstep=0.01
)

slider_delta = Slider(
    ax_delta,
    "delta: crecimiento de presión",
    0.01,
    0.3,
    valinit=delta0,
    valstep=0.01
)

slider_gamma = Slider(
    ax_gamma,
    "gamma: estabilización",
    0.01,
    1.0,
    valinit=gamma0,
    valstep=0.01
)

slider_dolares0 = Slider(
    ax_dolares0,
    "Dólares iniciales",
    1,
    30,
    valinit=dolares0,
    valstep=1
)

slider_presion0 = Slider(
    ax_presion0,
    "Presión inicial",
    1,
    30,
    valinit=presion0,
    valstep=1
)

slider_tiempo = Slider(
    ax_tiempo,
    "Tiempo",
    20,
    150,
    valinit=tiempo_final0,
    valstep=5
)


# ====================================================
# 7. Variables globales para animación
# ====================================================
estado = {
    "t": t,
    "dolares": dolares,
    "presion": presion,
    "frame": 0
}


# ====================================================
# 8. Función para actualizar cuando se mueven sliders
# ====================================================
def actualizar_modelo(val=None):
    alpha = slider_alpha.val
    beta = slider_beta.val
    delta = slider_delta.val
    gamma = slider_gamma.val

    dolares_iniciales = slider_dolares0.val
    presion_inicial = slider_presion0.val
    tiempo_final = slider_tiempo.val

    t, solucion = resolver_modelo(
        alpha,
        beta,
        delta,
        gamma,
        dolares_iniciales,
        presion_inicial,
        tiempo_final
    )

    dolares = solucion[:, 0]
    presion = solucion[:, 1]

    estado["t"] = t
    estado["dolares"] = dolares
    estado["presion"] = presion
    estado["frame"] = 0

    # Actualizar curvas del gráfico temporal
    linea_dolares.set_data(t, dolares)
    linea_presion.set_data(t, presion)

    axs[0].set_xlim(0, tiempo_final)
    axs[0].set_ylim(0, max(max(dolares), max(presion)) * 1.2)

    # Actualizar espacio de fase
    linea_fase.set_data(dolares, presion)

    axs[1].set_xlim(0, max(dolares) * 1.2)
    axs[1].set_ylim(0, max(presion) * 1.2)

    # Actualizar punto de equilibrio
    equilibrio_x = gamma / delta
    equilibrio_y = alpha / beta
    punto_equilibrio.set_offsets([[equilibrio_x, equilibrio_y]])

    texto_info.set_text(
        f"Equilibrio aproximado: "
        f"dólares = {equilibrio_x:.2f}, "
        f"presión = {equilibrio_y:.2f}"
    )

    fig.canvas.draw_idle()


# Conectar sliders
slider_alpha.on_changed(actualizar_modelo)
slider_beta.on_changed(actualizar_modelo)
slider_delta.on_changed(actualizar_modelo)
slider_gamma.on_changed(actualizar_modelo)
slider_dolares0.on_changed(actualizar_modelo)
slider_presion0.on_changed(actualizar_modelo)
slider_tiempo.on_changed(actualizar_modelo)


# ====================================================
# 9. Animación del movimiento
# ====================================================
def animar(frame):
    t = estado["t"]
    dolares = estado["dolares"]
    presion = estado["presion"]

    i = estado["frame"]

    if i >= len(t):
        i = 0
        estado["frame"] = 0

    # Punto móvil en gráfico temporal
    punto_dolares.set_data([t[i]], [dolares[i]])
    punto_presion.set_data([t[i]], [presion[i]])

    # Punto móvil en espacio de fase
    punto_fase.set_data([dolares[i]], [presion[i]])

    texto_info.set_text(
        f"Tiempo: {t[i]:.2f} | "
        f"Dólares: {dolares[i]:.2f} | "
        f"Presión: {presion[i]:.2f} | "
        f"alpha={slider_alpha.val:.2f}, "
        f"beta={slider_beta.val:.2f}, "
        f"delta={slider_delta.val:.2f}, "
        f"gamma={slider_gamma.val:.2f}"
    )

    estado["frame"] += 3

    return punto_dolares, punto_presion, punto_fase, texto_info


animacion = FuncAnimation(
    fig,
    animar,
    interval=40,
    blit=False
)


# ====================================================
# 10. Botón para reiniciar
# ====================================================
ax_boton = plt.axes([0.40, 0.005, 0.20, 0.03])
boton_reset = Button(ax_boton, "Reiniciar")


def reiniciar(event):
    slider_alpha.reset()
    slider_beta.reset()
    slider_delta.reset()
    slider_gamma.reset()
    slider_dolares0.reset()
    slider_presion0.reset()
    slider_tiempo.reset()
    actualizar_modelo()


boton_reset.on_clicked(reiniciar)


# 
# 11. Mostrar gráficos
# 
actualizar_modelo()
plt.show()