// --- NAVEGACIÓN Y EFECTOS VISUALES ---
const views = ['home', 'calc', 'lotka', 'covid', 'roulette'];
const bodyElement = document.getElementById('main-body');
const defaultBg = 'bg-green-50';
let currentBg = defaultBg;

function showView(viewId) {
    views.forEach(v => {
        document.getElementById(`view-${v}`).classList.add('hidden');
    });
    document.getElementById(`view-${viewId}`).classList.remove('hidden');
    
    // Acciones específicas al abrir ciertas vistas
    if(viewId === 'lotka' && !lotkaChartInstance) { runLotkaVolterra(); }
    if(viewId === 'covid') { drawCovidGrid(); }
    if(viewId === 'roulette') { drawRoulette(0); }
}

// Función para cambiar el fondo al pasar el mouse
function changeBackground(colorClass) {
    bodyElement.classList.remove(currentBg);
    bodyElement.classList.add(colorClass);
    currentBg = colorClass;
}

// Función para restaurar el fondo original al quitar el mouse
function resetBackground() {
    bodyElement.classList.remove(currentBg);
    bodyElement.classList.add(defaultBg);
    currentBg = defaultBg;
}


// 1. lotka

function lotkaVoltera(){
    eel.irLotkaVoltera()();
    window.close();
}

// 2. covid

function covid(){
    eel.irCovid()();
    window.close();
}

// 3. calculadora

function calculadora(){
    eel.irCalculadora()();
    window.close();
}

// 4. casino

function casino(){
    eel.irCasino()();
    window.close();
}

