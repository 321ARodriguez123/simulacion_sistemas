let currentRiList = [];

// 1. Cargar la librería de Google Charts al inicio
google.charts.load('current', {'packages':['corechart', 'bar', 'scatter']});

const configMetodos = {
    "Cuadrados Medios": ["semilla", "rango"],
    "Productos Medios": ["semilla1", "semilla2", "rango"],
    "Multiplicador Constante": ["a", "semilla", "rango"],
    "Congruencial Lineal": ["a", "c", "m", "semilla", "rango"]
};

// 2. CONFIGURACIÓN: Quitamos "Uniforme" de aquí para manejarlo manual y que no sea input
const configGraficos = {
    "Exponencial": [{ id: "lambda", label: "Tasa (λ):", val: "1.0" }],
    "Normal": [{ id: "mu", label: "Media (μ):", val: "0" }, { id: "sigma", label: "Desv (σ):", val: "1" }],
    "Gamma": [{ id: "alfa", label: "Forma (α):", val: "2.0" }, { id: "beta", label: "Escala (β):", val: "1.0" }],
    "k-Erlang": [{ id: "k", label: "Forma (k):", val: "2" }, { id: "lam_erlang", label: "Tasa (λ):", val: "1.0" }],
    "Weibull": [{ id: "k_w", label: "Forma (k):", val: "1.5" }, { id: "lam_w", label: "Escala (λ):", val: "1.0" }]
};

document.addEventListener("DOMContentLoaded", () => {
    actualizarInputsSimulacion();
    actualizarInputsGraficos();

    document.querySelectorAll('input[name="metodo"]').forEach(radio => {
        radio.addEventListener("change", actualizarInputsSimulacion);
    });

    document.getElementById("dist-select").addEventListener("change", actualizarInputsGraficos);
    document.getElementById("btn-generar").addEventListener("click", generarSimulacion);
    document.getElementById("btn-graficar").addEventListener("click", actualizarGraficos);
});

function actualizarInputsSimulacion() {
    const metodo = document.querySelector('input[name="metodo"]:checked').value;
    const container = document.getElementById("dynamic-inputs");
    container.innerHTML = "";
    configMetodos[metodo].forEach(campo => {
        const div = document.createElement("div");
        div.className = "input-group";
        div.innerHTML = `<label>${campo.toUpperCase()}:</label><input type="number" id="input-${campo}" value="${campo === 'rango' ? 10 : ''}" required>`;
        container.appendChild(div);
    });
}

function actualizarInputsGraficos() {
    const dist = document.getElementById("dist-select").value;
    const container = document.getElementById("chart-inputs");
    container.innerHTML = "";
    
    // CASO ESPECIAL: Uniforme. Calcula el min/max real y los muestra como texto.
    if (dist === "Uniforme") {
        let min = "0.0000";
        let max = "1.0000";
        
        // Si ya hay datos generados, sacamos el mínimo y máximo real
        if (currentRiList && currentRiList.length > 0) {
            min = Math.min(...currentRiList).toFixed(4);
            max = Math.max(...currentRiList).toFixed(4);
        }

        container.innerHTML = `
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:0.85rem; font-weight:600; color: #64748b;">Min:</span>
                <span style="font-weight:bold; color: #22c55e;">${min}</span>
                <input type="hidden" id="g-input-a" value="${min}">
            </div>
            <div style="display:flex; align-items:center; gap:8px; margin-left: 10px;">
                <span style="font-size:0.85rem; font-weight:600; color: #64748b;">Max:</span>
                <span style="font-weight:bold; color: #22c55e;">${max}</span>
                <input type="hidden" id="g-input-b" value="${max}">
            </div>
        `;
    } 
    // Para el resto de distribuciones sí se dibujan los inputs
    else if (configGraficos[dist]) {
        configGraficos[dist].forEach(campo => {
            container.innerHTML += `<div style="display:flex; align-items:center; gap:5px;"><label style="font-size:0.85rem; font-weight:600; color:#4b5563;">${campo.label}</label><input type="number" step="0.1" id="g-input-${campo.id}" value="${campo.val}" style="width: 70px; padding: 5px; border: 1px solid #d1d5db; border-radius: 6px;"></div>`;
        });
    }
}

async function generarSimulacion() {
    const btn = document.getElementById("btn-generar");
    const textoOriginal = btn.innerHTML; 
    
    btn.disabled = true;
    btn.innerHTML = "⏳ Procesando...";

    try {
        const metodo = document.querySelector('input[name="metodo"]:checked').value;
        const params = {};
        configMetodos[metodo].forEach(campo => {
            params[campo] = document.getElementById(`input-${campo}`).value;
        });

        const response = await eel.generar_simulacion(metodo, params)();
        
        if (response.status === "error") {
            alert("Error: " + response.message);
            return;
        }

        currentRiList = response.ri_list;
        
        const emptyState = document.getElementById("stats-empty");
        const contentState = document.getElementById("stats-content");

        if (response.stats) {
            const s = response.stats;
            
            emptyState.style.display = "none";
            contentState.style.display = "flex";

            document.getElementById("media-val").innerText = s.media.val;
            document.getElementById("media-tol").innerText = s.media.tol;
            const mediaStatus = document.getElementById("media-status");
            mediaStatus.innerText = s.media.texto;
            mediaStatus.className = `status-indicator ${s.media.clase}`;

            document.getElementById("var-val").innerText = s.varianza.val;
            document.getElementById("var-esp").innerText = s.varianza.esp;
            const varStatus = document.getElementById("var-status");
            varStatus.innerText = s.varianza.texto;
            varStatus.className = `status-indicator ${s.varianza.clase}`;

            document.getElementById("unif-val").innerText = s.uniformidad.p;
            const unifStatus = document.getElementById("unif-status");
            unifStatus.innerText = s.uniformidad.texto;
            unifStatus.className = `status-indicator ${s.uniformidad.clase}`;

        } else {
            emptyState.style.display = "block";
            emptyState.innerText = "Sin datos generados.";
            contentState.style.display = "none";
        }

        dibujarTabla(response.filas);
        
        // Refrescamos los textos por si estaba seleccionada la Uniforme
        actualizarInputsGraficos();
        await actualizarGraficos(); 
        
    } catch (error) {
        alert("Error de conexión con Python.");
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.innerHTML = textoOriginal;
    }
}

async function actualizarGraficos() {
    if (currentRiList.length === 0) return;

    const btn = document.getElementById("btn-graficar");
    const textoOriginal = btn.innerHTML;
    
    btn.disabled = true;
    btn.innerHTML = "⏳ Graficando...";

    try {
        const distribucion = document.getElementById("dist-select").value;
        const params = {};
        
        // Especial para Uniforme: recogemos los valores de los inputs ocultos
        if (distribucion === "Uniforme") {
            params["a"] = document.getElementById("g-input-a").value;
            params["b"] = document.getElementById("g-input-b").value;
        } else if(configGraficos[distribucion]) {
            configGraficos[distribucion].forEach(campo => {
                params[campo.id] = document.getElementById(`g-input-${campo.id}`).value;
            });
        }

        // NUEVO: Capturamos la cantidad de rangos deseados
        params["rangos"] = document.getElementById("g-input-rangos").value;
        // Aquí es donde se envía todo a Python
        const response = await eel.procesar_graficos(currentRiList, distribucion, params)();
        
        if (response.status === "error") {
            alert(response.message);
            return;
        }

        google.charts.setOnLoadCallback(() => {
            dibujarHistogramaGC(response.titulo, response.hist_labels, response.hist_data);
            dibujarDispersionGC(response.scatter_data);
        });
    } catch (error) {
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.innerHTML = textoOriginal;
    }
}

function dibujarTabla(filas) {
    const thead = document.getElementById("table-head");
    const tbody = document.getElementById("table-body");
    thead.innerHTML = ""; tbody.innerHTML = "";
    if (filas.length === 0) return;

    const colCount = filas[0].length;
    let headers = ["Iteración", "Valor 1", "Valor 2", "Resultado", "Centro", "Ri"].slice(0, colCount);
    if(colCount === 4) headers = ["Iteración", "Semilla", "Resultado", "Ri"]; 

    headers.forEach(h => thead.innerHTML += `<th>${h}</th>`);
    filas.forEach(fila => {
        const tr = document.createElement("tr");
        fila.forEach(celda => tr.innerHTML += `<td>${celda}</td>`);
        tbody.appendChild(tr);
    });
}

function dibujarHistogramaGC(titulo, labels, data) {
    const dataTable = new google.visualization.DataTable();
    dataTable.addColumn('string', 'Intervalo');
    dataTable.addColumn('number', 'Frecuencia');
    
    const filasFormateadas = labels.map((label, i) => [label, data[i]]);
    dataTable.addRows(filasFormateadas);

    const options = {
        title: titulo,
        titleTextStyle: { fontSize: 16, color: '#0f172a' },
        legend: { position: 'none' },
        colors: ['#22c55e'], 
        bar: { groupWidth: '98%' }, 
        hAxis: { 
            title: 'Rangos', 
            slantedText: true, 
            slantedTextAngle: 45
        },
        vAxis: { title: 'Frecuencia', minValue: 0 },
        chartArea: { width: '85%', height: '65%' },
        animation: { startup: true, duration: 500, easing: 'out' }
    };

    const chart = new google.visualization.ColumnChart(document.getElementById('histChart'));
    chart.draw(dataTable, options);
}

function dibujarDispersionGC(dataObjects) {
    const dataTable = new google.visualization.DataTable();
    dataTable.addColumn('number', 'Ri');
    dataTable.addColumn('number', 'Ri+1');

    const filasFormateadas = dataObjects.map(obj => [obj.x, obj.y]);
    dataTable.addRows(filasFormateadas);

    const options = {
        title: 'Dispersión (Ri vs Ri+1)',
        titleTextStyle: { fontSize: 16, color: '#0f172a' },
        hAxis: { title: 'Ri' },
        vAxis: { title: 'Ri+1' },
        legend: 'none',
        colors: ['#f59e0b'],
        pointSize: 4,
        chartArea: { width: '80%', height: '70%' },
        animation: { startup: true, duration: 500, easing: 'out' }
    };

    const chart = new google.visualization.ScatterChart(document.getElementById('scatterChart'));
    chart.draw(dataTable, options);
}

function irInicio(){
    eel.irInicio()();
    window.close();
}