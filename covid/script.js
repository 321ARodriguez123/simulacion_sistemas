const canvas = document.getElementById('tablero');
const ctx = canvas.getContext('2d');
const cellSize = 8;
const cols = Math.floor(canvas.width / cellSize);
const rows = Math.floor(canvas.height / cellSize);

let pausado = false;

const colores = {
    0: '#0F0F0F', 
    1: '#64C8FF', 
    2: '#FF3232', 
    3: '#787878', 
    4: '#6a006a'  
};

function dibujarTablero(grid) {
    ctx.fillStyle = colores[0];
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            let state = grid[y][x];
            if (state !== 0) {
                ctx.fillStyle = colores[state];
                ctx.fillRect(x * cellSize, y * cellSize, cellSize - 1, cellSize - 1);
            }
        }
    }
}

function actualizarUI(stats, dia) {
    document.getElementById('lbl-dia').innerText = dia;
    document.getElementById('lbl-sanos').innerText = stats.sanos;
    document.getElementById('lbl-inf').innerText = stats.infectados;
    document.getElementById('lbl-rec').innerText = stats.recuperados;
    document.getElementById('lbl-mue').innerText = stats.muertos;
}

// Bucle principal
async function loop() {
    if (!pausado) {
        // Llamada a Python usando Eel (nota los dobles paréntesis)
        let data = await eel.next_frame()();
        dibujarTablero(data.grid);
        actualizarUI(data.stats, data.dia);
    }
    setTimeout(loop, 66);
}

// Eventos
document.getElementById('btn-pausa').addEventListener('click', () => {
    pausado = !pausado;
    document.getElementById('btn-pausa').innerText = pausado ? "▶ Reanudar" : "⏸ Pausar";
});

document.getElementById('btn-reiniciar').addEventListener('click', async () => {
    let data = await eel.reset_simulation()();
    dibujarTablero(data.grid);
    actualizarUI(data.stats, data.dia);
});

// Inicialización directa (Eel carga muy rápido, no necesitamos event listeners complejos)
async function arrancarApp() {
    let data = await eel.get_initial_state()();
    dibujarTablero(data.grid);
    actualizarUI(data.stats, data.dia);
    loop();
}

arrancarApp();