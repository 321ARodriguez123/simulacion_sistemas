# Portal de Simuladores Interactivo

**Área/Materia:** Simulación de Sistemas  
**Desarrollador:** Diego Adrian Rodriguez Quispe  
**Institución:** Universidad San Francisco de Asís (USFA) - La Paz, Bolivia  

## 📖 Descripción del Proyecto
Este proyecto es una plataforma interactiva de simulación de escritorio desarrollada con una arquitectura de múltiples procesos. Utiliza **Python** como motor lógico (Backend) y tecnologías web (**HTML, CSS, JavaScript**) para la interfaz gráfica (Frontend), comunicados a través de la librería **Eel**. 

El portal actúa como un menú principal que permite al usuario navegar y ejecutar de manera independiente cuatro herramientas de simulación distintas, aislando los procesos en memoria para garantizar un rendimiento óptimo.

## 🚀 Módulos del Sistema

El ecosistema está compuesto por un menú central y 4 submódulos independientes:

1. **Simulador Lotka-Volterra (Dinámica de Poblaciones)**
   * Simulación matemática de la interacción entre depredadores (lobos) y presas (ovejas).
   * **Motor:** Resuelve ecuaciones diferenciales ordinarias (EDO) utilizando `scipy.integrate.odeint`.
   * **Visualización:** Gráficos en tiempo real del espacio de fase y la dinámica poblacional en el tiempo.

2. **Simulador de Propagación (COVID / Autómata Celular)**
   * Basado en las reglas del "Juego de la Vida" de Conway, adaptado para modelar la propagación de contagios en una cuadrícula.
   * Procesamiento visual directamente en un elemento `<canvas>` de HTML5 con actualizaciones por intervalos de tiempo.

3. **Ruleta de Casino (Simulación Probabilística)**
   * Motor de probabilidad y gestión de estados (saldo, ganancias, pérdidas, historial) controlado por Python.
   * Interfaz gráfica interactiva con tablero de apuestas completo, animaciones de físicas de giro y cálculo automático de retornos de inversión según el tipo de apuesta.

4. **Calculadora**
   * Herramienta utilitaria integrada de cálculos rápidos con validación de errores matemáticos.

## 🛠️ Tecnologías y Librerías

* **Backend:** Python 3.x
* **Puente (Bridge):** [Eel](https://github.com/python-eel/Eel) (Para renderizar la interfaz web como una app de escritorio nativa).
* **Cálculo Científico:** `scipy`, `numpy`.
* **Procesamiento del Sistema:** `subprocess`, `os`, `sys` (Para la gestión y destrucción de procesos al cambiar de submódulo).
* **Frontend:** HTML5, CSS3 puro (Diseño minimalista) y Vanilla JavaScript.
* **Gráficos:** Google Charts / Chart.js.

## 📁 Estructura del Proyecto

```text
Simulacion de sistemas/
│
├── main.py                   # Menú principal (Enrutador de procesos)
├── web/                      # Frontend del menú principal
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── Lotka/                    # Módulo Dinámica de Poblaciones
│   ├── main.py
│   └── web/
│
├── covid/                    # Módulo Autómata Celular
│   ├── main.py
│   └── web/
│
├── Ruleta/                   # Módulo Probabilístico
│   ├── main.py
│   └── web/
│
└── Calculadora/              # Módulo Matemático
    ├── main.py
    └── web/




⚙️ Instalación y Requisitos
Asegúrate de tener Python 3.8+ instalado en tu sistema.

Es necesario tener instalado Google Chrome o Microsoft Edge para que Eel renderice la ventana correctamente.

Instala las dependencias necesarias ejecutando el siguiente comando en tu terminal:
### ⚙️ Instalación de Librerías

Este proyecto contiene un archivo llamado `requirements.txt`. Este archivo tiene la lista exacta de todas las librerías principales (Eel, Scipy, Numpy) y sus dependencias internas necesarias para que los simuladores funcionen correctamente.

Para instalar todo automáticamente, abre la terminal en la carpeta de este proyecto y ejecuta este único comando:

```bash
pip install -r requirements.txt