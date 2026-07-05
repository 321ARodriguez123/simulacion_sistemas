// 1. Cargar la librería corechart de Google
google.charts.load('current', {'packages':['corechart']});

let timeChart = null;
let phaseChart = null;
let timeOptions = {};
let phaseOptions = {};

// Arreglos para almacenar el historial de puntos
let timeDataArray = [];
let phaseDataArray = [];
const MAX_PUNTOS = 200;

// 2. Esperar a que Google Charts termine de cargar antes de permitir clics
google.charts.setOnLoadCallback(() => {
    document.getElementById('btn-iniciar').disabled = false;
    document.getElementById('info-bar').innerText = "Listo para iniciar. Presiona 'Reiniciar Simulación'.";
    iniciar(); // Auto-iniciar
});

// Configurar sliders para actualizar texto y enviar datos a Python en vivo
document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', (e) => {
        document.getElementById(`val_${e.target.id}`).innerText = e.target.value;
        const alpha = parseFloat(document.getElementById('alpha').value);
        const beta = parseFloat(document.getElementById('beta').value);
        const delta = parseFloat(document.getElementById('delta').value);
        const gamma = parseFloat(document.getElementById('gamma').value);
        eel.actualizar_parametros(alpha, beta, delta, gamma)();
    });
});

function inicializarGraficos() {
    timeChart = new google.visualization.LineChart(document.getElementById('timeChart'));
    phaseChart = new google.visualization.ScatterChart(document.getElementById('phaseChart'));

    // Configuración estética del gráfico de Tiempo
    timeOptions = {
        animation: { duration: 0 }, // Importante en 0 para tiempo real sin parpadeos
        legend: { position: 'bottom' },
        colors: ['#3498db', '#e67e22'],
        chartArea: { width: '85%', height: '70%' },
        hAxis: { title: 'Tiempo' },
        vAxis: { title: 'Población', viewWindow: { min: 0 } },
        lineWidth: 2
    };

    // Configuración estética del Espacio de Fase
    phaseOptions = {
        animation: { duration: 0 },
        legend: { position: 'bottom' },
        colors: ['#2980b9', '#e74c3c', '#27ae60'],
        chartArea: { width: '85%', height: '70%' },
        hAxis: { title: 'Ovejas (Presas)', viewWindow: { min: 0 } },
        vAxis: { title: 'Lobos (Depredadores)', viewWindow: { min: 0 } },
        series: {
            0: { lineWidth: 2, pointSize: 0 }, // Trayectoria: Línea continua, sin puntos
            1: { lineWidth: 0, pointSize: 8 }, // Estado Actual: Solo el punto rojo
            2: { lineWidth: 0, pointSize: 10, pointShape: 'square' } // Equilibrio: Cuadrado verde
        }
    };

    // Reiniciar los encabezados de las tablas
    timeDataArray = [['Tiempo', 'Ovejas', 'Lobos']];
    phaseDataArray = [['Ovejas', 'Trayectoria', 'Estado Actual', 'Equilibrio']];
}

eel.expose(recibir_nuevo_punto);
function recibir_nuevo_punto(t, ovejas, lobos, eq_ovejas, eq_lobos, alpha, beta, delta, gamma) {
    if (!timeChart || !phaseChart) return;

    // Actualizar texto central
    document.getElementById('info-bar').innerText = 
        `Tiempo: ${t.toFixed(2)} | Ovejas: ${ovejas.toFixed(2)} | Lobos: ${lobos.toFixed(2)} | alpha=${alpha}, beta=${beta}, delta=${delta}, gamma=${gamma}`;

    // --- GRÁFICO DE TIEMPO ---
    timeDataArray.push([t, ovejas, lobos]);
    if (timeDataArray.length > MAX_PUNTOS + 1) { // +1 por la fila del encabezado
        timeDataArray.splice(1, 1);
    }
    const dtTime = google.visualization.arrayToDataTable(timeDataArray);
    timeChart.draw(dtTime, timeOptions);


    // --- GRÁFICO DE FASE ---
    // Guardamos la trayectoria histórica (los null evitan que se dibujen los puntos sueltos aquí)
    phaseDataArray.push([ovejas, lobos, null, null]);
    if (phaseDataArray.length > MAX_PUNTOS + 1) {
        phaseDataArray.splice(1, 1);
    }

    // Creamos una copia temporal de la trayectoria para agregarle los dos puntos flotantes
    let currentPhaseData = [...phaseDataArray];
    
    // Agregamos la coordenada del "Estado Actual" (columna 3)
    currentPhaseData.push([ovejas, null, lobos, null]);
    
    // Agregamos la coordenada del "Punto de Equilibrio" (columna 4)
    currentPhaseData.push([eq_ovejas, null, null, eq_lobos]);

    const dtPhase = google.visualization.arrayToDataTable(currentPhaseData);
    phaseChart.draw(dtPhase, phaseOptions);
}

function iniciar() {
    inicializarGraficos();
    const a = parseFloat(document.getElementById('alpha').value);
    const b = parseFloat(document.getElementById('beta').value);
    const d = parseFloat(document.getElementById('delta').value);
    const g = parseFloat(document.getElementById('gamma').value);
    const ov0 = parseFloat(document.getElementById('ovejas0').value);
    const lo0 = parseFloat(document.getElementById('lobos0').value);
    
    eel.iniciar_simulacion(a, b, d, g, ov0, lo0)();
}

function detener() { 
    eel.detener_simulacion()(); 
}