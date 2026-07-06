google.charts.load('current', {'packages':['corechart']});

let timeChart = null;
let phaseChart = null;
let timeOptions = {};
let phaseOptions = {};

let timeDataArray = [];
let phaseDataArray = [];
const MAX_PUNTOS = 200;

google.charts.setOnLoadCallback(() => {
    document.getElementById('btn-iniciar').disabled = false;
    document.getElementById('info-bar').innerText = "Listo para iniciar. Presiona 'Reiniciar Simulación'.";
    iniciar(); 
});

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

    timeOptions = {
        animation: { duration: 0 }, 
        legend: { position: 'bottom' },
        colors: ['#4ade80', '#9ca3af'], 
        chartArea: { width: '85%', height: '70%' },
        hAxis: { title: 'Tiempo' },
        vAxis: { title: 'Población', viewWindow: { min: 0 } },
        lineWidth: 2,
        curveType: 'function' 
    };

    phaseOptions = {
        animation: { duration: 0 },
        legend: { position: 'bottom' },
        colors: ['#4ade80', '#dc2626', '#16a34a'], 
        chartArea: { width: '85%', height: '70%' },
        hAxis: { title: 'Ovejas (Presas)', viewWindow: { min: 0 } },
        vAxis: { title: 'Lobos (Depredadores)', viewWindow: { min: 0 } },
        curveType: 'function', 
        series: {
            0: { lineWidth: 2, pointSize: 0 }, 
            1: { lineWidth: 0, pointSize: 8 }, 
            2: { lineWidth: 0, pointSize: 10, pointShape: 'square' } 
        }
    };

    timeDataArray = [['Tiempo', 'Ovejas', 'Lobos']];
    phaseDataArray = [['Ovejas', 'Trayectoria', 'Estado Actual', 'Equilibrio']];
}

eel.expose(recibir_nuevo_punto);
function recibir_nuevo_punto(t, ovejas, lobos, eq_ovejas, eq_lobos, alpha, beta, delta, gamma) {
    if (!timeChart || !phaseChart) return;

    document.getElementById('info-bar').innerText = 
        `T: ${t.toFixed(1)} | Ov: ${ovejas.toFixed(1)} | Lo: ${lobos.toFixed(1)} | α=${alpha}, β=${beta}, δ=${delta}, γ=${gamma}`;

    // Gráfico de tiempo
    timeDataArray.push([t, ovejas, lobos]);
    if (timeDataArray.length > MAX_PUNTOS + 1) timeDataArray.splice(1, 1);
    const dtTime = google.visualization.arrayToDataTable(timeDataArray);
    timeChart.draw(dtTime, timeOptions);

    // Gráfico de fase
    phaseDataArray.push([ovejas, lobos, null, null]);
    if (phaseDataArray.length > MAX_PUNTOS + 1) phaseDataArray.splice(1, 1);

    let currentPhaseData = [...phaseDataArray];
    currentPhaseData.push([ovejas, null, lobos, null]);
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

function detener() { eel.detener_simulacion()(); }