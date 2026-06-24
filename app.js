/* ==========================================================================
   LÓGICA DE SIMULACIÓN HIDRÁULICA Y GRÁFICOS - DML INGENIEROS CONSULTORES
   ========================================================================== */

// 1. Datos Topográficos del Perfil del Cruce (Plano 202609-BRI-SE-CIV-PL-001-RB)
const perfilDatos = [
    { abscisa: 0, terreno: 2558.37, clavePHD: 2558.35 },
    { abscisa: 10, terreno: 2558.18, clavePHD: 2555.85 },
    { abscisa: 20, terreno: 2558.18, clavePHD: 2553.36 },
    { abscisa: 30, terreno: 2558.18, clavePHD: 2550.87 },
    { abscisa: 40, terreno: 2558.16, clavePHD: 2548.37 },
    { abscisa: 50, terreno: 2557.75, clavePHD: 2545.88 },
    { abscisa: 60, terreno: 2557.73, clavePHD: 2543.86 },
    { abscisa: 70, terreno: 2557.79, clavePHD: 2542.87 },
    { abscisa: 80, terreno: 2557.71, clavePHD: 2542.75 },
    { abscisa: 90, terreno: 2557.61, clavePHD: 2542.75 },
    { abscisa: 100, terreno: 2557.52, clavePHD: 2542.75 },
    { abscisa: 110, terreno: 2557.66, clavePHD: 2542.75 },
    { abscisa: 120, terreno: 2557.57, clavePHD: 2542.75 },
    { abscisa: 130, terreno: 2557.55, clavePHD: 2542.75 },
    { abscisa: 140, terreno: 2557.56, clavePHD: 2542.75 },
    { abscisa: 150, terreno: 2557.52, clavePHD: 2542.75 },
    { abscisa: 160, terreno: 2557.59, clavePHD: 2542.75 },
    { abscisa: 170, terreno: 2557.67, clavePHD: 2542.75 },
    { abscisa: 180, terreno: 2557.70, clavePHD: 2542.75 },
    { abscisa: 190, terreno: 2557.70, clavePHD: 2542.75 },
    { abscisa: 200, terreno: 2557.86, clavePHD: 2542.75 },
    { abscisa: 210, terreno: 2557.89, clavePHD: 2542.75 },
    { abscisa: 220, terreno: 2557.92, clavePHD: 2542.75 },
    { abscisa: 230, terreno: 2557.89, clavePHD: 2542.75 },
    { abscisa: 240, terreno: 2557.90, clavePHD: 2542.75 },
    { abscisa: 250, terreno: 2557.96, clavePHD: 2542.75 },
    { abscisa: 260, terreno: 2558.10, clavePHD: 2542.75 },
    { abscisa: 270, terreno: 2558.33, clavePHD: 2545.88 },
    { abscisa: 280, terreno: 2558.50, clavePHD: 2548.63 },
    { abscisa: 290, terreno: 2558.63, clavePHD: 2551.12 },
    { abscisa: 300, terreno: 2558.84, clavePHD: 2553.80 },
    { abscisa: 310, terreno: 2558.87, clavePHD: 2555.87 },
    { abscisa: 320, terreno: 2558.98, clavePHD: 2557.06 },
    { abscisa: 330, terreno: 2559.12, clavePHD: 2557.20 },
    { abscisa: 340, terreno: 2558.98, clavePHD: 2557.56 },
    { abscisa: 350, terreno: 2558.80, clavePHD: 2557.79 },
    { abscisa: 360, terreno: 2558.77, clavePHD: 2558.10 },
    { abscisa: 370, terreno: 2558.78, clavePHD: 2558.10 },
    { abscisa: 380, terreno: 2558.97, clavePHD: 2558.10 },
    { abscisa: 390, terreno: 2558.76, clavePHD: 2557.58 },
    { abscisa: 400, terreno: 2558.98, clavePHD: 2557.56 },
    { abscisa: 410, terreno: 2558.99, clavePHD: 2557.56 },
    { abscisa: 420, terreno: 2558.80, clavePHD: 2557.56 },
    { abscisa: 430, terreno: 2558.90, clavePHD: 2557.56 },
    { abscisa: 440, terreno: 2558.92, clavePHD: 2557.56 },
    { abscisa: 450, terreno: 2557.56, clavePHD: 2557.56 }
];

// Constantes Físicas
const G = 9.80665;
const RUGOSIDAD_HDPE = 1.5e-6; // m

// Propiedades de los Fluidos
const FLUIDOS = {
    salmuera: {
        nombre: "Salmuera Saturada (26% NaCl)",
        densidad: 1200.0, // kg/m^3
        viscosidad: 0.0016 // Pa*s (1.6 cP)
    },
    condensado: {
        nombre: "Condensado (Agua Industrial)",
        densidad: 1000.0, // kg/m^3
        viscosidad: 0.0010 // Pa*s (1.0 cP)
    }
};

// Dimensiones de Tuberías HDPE PE100 SDR 17 (Caso base nominal)
// Diámetros exteriores (OD) según estándar métrico
const TUBERIAS_INFO = {
    8: { OD: 0.225, nominalName: "8\" NPS (OD 225 mm)" },
    10: { OD: 0.280, nominalName: "10\" NPS (OD 280 mm)" },
    12: { OD: 0.315, nominalName: "12\" NPS (OD 315 mm)" }
};

// Variables globales de gráficos de Chart.js
let chartProfileInstance = null;
let chartPressureInstance = null;
let chartLossInstance = null;

// Inicialización de la Aplicación
document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
    actualizarSimulacion();
    inicializarGraficoPerfil();
});

// Event Listeners de los Controles
function setupEventListeners() {
    const inputs = ["flow-rate", "pipe-dia", "pipe-sdr", "sim-scenario", "inlet-pressure"];
    inputs.forEach(id => {
        const el = document.getElementById(id);
        el.addEventListener("input", actualizarSimulacion);
        el.addEventListener("change", actualizarSimulacion);
    });

    const radios = document.getElementsByName("fluidType");
    radios.forEach(radio => {
        radio.addEventListener("change", actualizarSimulacion);
    });
}

// Factor de Fricción de Darcy usando aproximación de Haaland
function calcularFriccionHaaland(Re, roughnessRatio) {
    if (Re < 2300) {
        return 64.0 / Re;
    } else {
        const termino = Math.pow((roughnessRatio / 3.7), 1.11) + 6.9 / Re;
        const invSqrtF = -1.8 * Math.log10(termino);
        return 1.0 / Math.pow(invSqrtF, 2);
    }
}

// Lógica Principal de Simulación
function actualizarSimulacion() {
    // 1. Capturar parámetros de la interfaz
    const fluidType = document.querySelector('input[name="fluidType"]:checked').value;
    const flujoMasico = parseFloat(document.getElementById("flow-rate").value);
    const nps = parseInt(document.getElementById("pipe-dia").value);
    const sdr = parseFloat(document.getElementById("pipe-sdr").value);
    const simScenario = document.getElementById("sim-scenario").value;
    const inletPresSurface = parseFloat(document.getElementById("inlet-pressure").value); // bar

    // Actualizar visualizaciones de valores en los textos
    document.getElementById("flow-val").innerText = flujoMasico.toLocaleString() + " kg/h";
    document.getElementById("pressure-val").innerText = inletPresSurface.toFixed(1) + " bar";

    const fluido = FLUIDOS[fluidType];
    const rho = fluido.densidad;
    const mu = fluido.viscosidad;

    // Calcular dimensiones internas basadas en SDR
    const pipeInfo = TUBERIAS_INFO[nps];
    const OD = pipeInfo.OD;
    const espesor = OD / sdr;
    const ID = OD - 2 * espesor;

    // Caudal volumétrico
    const Q = (flujoMasico / rho) / 3600.0; // m^3/s
    const Q_m3h = Q * 3600.0;
    const area = (Math.PI / 4.0) * Math.pow(ID, 2);
    const v = Q / area; // m/s

    const Re = (rho * v * ID) / mu;
    const roughnessRatio = RUGOSIDAD_HDPE / ID;
    const f = calcularFriccionHaaland(Re, roughnessRatio);

    // 2. Discretización punto a punto a lo largo del perfil topográfico
    let L_sup_acum = 0;
    let L_phd_acum = 0;
    
    const presionesPHD = [];
    const presionesSup = [];
    const cotasClavePHD = [];
    const cotasClaveSup = [];
    const abscisas = [];
    
    // Altura clave inicial (K0+000)
    const z_lanzamiento = perfilDatos[0].clavePHD;
    const z_origen_sesquile = 2703.37;

    // Coeficientes de pérdidas menores
    const K_sup = 0.2;
    const K_phd = 0.5;

    // Presión de entrada en Pascales (Dinámica)
    const P_inlet_pa = inletPresSurface * 1e5;

    for (let i = 0; i < perfilDatos.length; i++) {
        const punto = perfilDatos[i];
        abscisas.push("K" + punto.abscisa.toString().padStart(3, "0"));
        cotasClavePHD.push(punto.clavePHD);
        
        // El trazado superficial sigue al terreno a una distancia de 1.0 m, excepto extremos
        let claveSup = punto.terreno - 1.0;
        if (i === 0) claveSup = punto.clavePHD;
        if (i === perfilDatos.length - 1) claveSup = punto.clavePHD;
        cotasClaveSup.push(claveSup);

        if (i > 0) {
            const puntoAnt = perfilDatos[i - 1];
            let claveSupAnt = puntoAnt.terreno - 1.0;
            if (i - 1 === 0) claveSupAnt = puntoAnt.clavePHD;

            // Longitud infinitesimal superficial
            const dL_sup = Math.sqrt(
                Math.pow(punto.abscisa - puntoAnt.abscisa, 2) +
                Math.pow(claveSup - claveSupAnt, 2)
            );
            L_sup_acum += dL_sup;

            // Longitud infinitesimal PHD
            const dL_phd = Math.sqrt(
                Math.pow(punto.abscisa - puntoAnt.abscisa, 2) +
                Math.pow(punto.clavePHD - puntoAnt.clavePHD, 2)
            );
            L_phd_acum += dL_phd;
        }

        // Pérdida acumulada por fricción en el punto i
        const h_f_sup = f * (L_sup_acum / ID) * (Math.pow(v, 2) / (2 * G));
        const h_f_phd = f * (L_phd_acum / ID) * (Math.pow(v, 2) / (2 * G));

        // Pérdida menor prorrateada por longitud
        const h_m_sup = K_sup * (Math.pow(v, 2) / (2 * G)) * (i / (perfilDatos.length - 1));
        const h_m_phd = K_phd * (Math.pow(v, 2) / (2 * G)) * (i / (perfilDatos.length - 1));

        const h_L_sup = h_f_sup + h_m_sup;
        const h_L_phd = h_f_phd + h_m_phd;

        // Presión dinámica operativa
        const P_dyn_sup_pa = P_inlet_pa - rho * G * h_L_sup + rho * G * (z_lanzamiento - claveSup);
        const P_dyn_phd_pa = P_inlet_pa - rho * G * h_L_phd + rho * G * (z_lanzamiento - punto.clavePHD);

        // Presión estática en parada (sifón lleno)
        let P_est_sup_pa = 0;
        let P_est_phd_pa = 0;
        if (simScenario === "global") {
            // Referencia a Mina de Sesquilé
            P_est_sup_pa = rho * G * (z_origen_sesquile - claveSup);
            P_est_phd_pa = rho * G * (z_origen_sesquile - punto.clavePHD);
        } else {
            // Referencia a cota local de lanzamiento
            P_est_sup_pa = 0;
            P_est_phd_pa = rho * G * (z_lanzamiento - punto.clavePHD);
        }

        // Presión de diseño interna (máxima entre estática en parada y dinámica operativa)
        const P_sup_pa = Math.max(P_dyn_sup_pa, P_est_sup_pa);
        const P_phd_pa = Math.max(P_dyn_phd_pa, P_est_phd_pa);

        presionesSup.push(P_sup_pa / 1e5); // Convertir a bar
        presionesPHD.push(P_phd_pa / 1e5); // Convertir a bar
    }

    // 3. Actualizar KPIs en el Dashboard
    const dP_sup_total = (presionesSup[0] - presionesSup[presionesSup.length - 1]) * 100.0; // kPa
    const dP_phd_total = (presionesPHD[0] - presionesPHD[presionesPHD.length - 1]) * 100.0; // kPa
    const inc_dp_pct = ((dP_phd_total - dP_sup_total) / dP_sup_total) * 100.0;
    const inc_dp_val = dP_phd_total - dP_sup_total; // kPa

    document.getElementById("kpi-vel").innerText = v.toFixed(2);
    document.getElementById("kpi-dp-sup").innerText = dP_sup_total.toFixed(2);
    document.getElementById("kpi-dp-sup-bar").innerText = (dP_sup_total / 100.0).toFixed(3) + " bar";
    document.getElementById("kpi-dp-phd").innerText = dP_phd_total.toFixed(2);
    document.getElementById("kpi-dp-phd-bar").innerText = (dP_phd_total / 100.0).toFixed(3) + " bar";
    document.getElementById("kpi-inc-pct").innerText = inc_dp_pct.toFixed(2);
    document.getElementById("kpi-inc-val").innerText = "+" + inc_dp_val.toFixed(2) + " kPa";

    // 4. Evaluar y Actualizar Alertas Operativas
    actualizarAlertas(v, presionesPHD, sdr);

    // 5. Actualizar los gráficos interactivos
    actualizarGraficoPresiones(abscisas, presionesPHD, presionesSup, sdr);
    actualizarGraficoPerdidas(ID, K_sup, K_phd, rho, mu);
}

// Control de Alertas
function actualizarAlertas(v, presionesPHD, sdr) {
    // Límite de Presión Nominal (PN) según SDR del tubo HDPE PE100
    const limitesSDR = {
        7.4: 25.0,
        9: 20.0,
        11: 16.0,
        13.6: 12.5,
        17: 10.0,
        21: 8.0
    };
    const pn_limite = limitesSDR[sdr];

    // Presión máxima en el fondo (el punto más profundo es el índice 26, abscisa K260)
    const P_max_fondo = Math.max(...presionesPHD);

    // Alerta 1: Sedimentación (v < 0.9 m/s)
    const alertSed = document.getElementById("alert-sedimentation");
    const msgSed = document.getElementById("alert-sed-msg");
    if (v < 0.9) {
        alertSed.className = "alert-card alert-danger";
        msgSed.innerText = `Riesgo Alto. V = ${v.toFixed(2)} m/s (Límite autolimpieza: 0.9 m/s). Riesgo de obstrucción de sal o arena en fondo.`;
    } else {
        alertSed.className = "alert-card alert-success";
        msgSed.innerText = `Velocidad segura: ${v.toFixed(2)} m/s. Tránsito turbulento óptimo para arrastre.`;
    }

    // Alerta 2: Erosión (v > 3.0 m/s)
    const alertEro = document.getElementById("alert-erosion");
    const msgEro = document.getElementById("alert-ero-msg");
    if (v > 3.0) {
        alertEro.className = "alert-card alert-danger";
        msgEro.innerText = `Riesgo Alto. V = ${v.toFixed(2)} m/s (Límite erosión: 3.0 m/s). Riesgo de desgaste acelerado de tubería.`;
    } else if (v > 2.2) {
        alertEro.className = "alert-card alert-warning";
        msgEro.innerText = `Precaución. V = ${v.toFixed(2)} m/s. Pérdidas dinámicas elevadas.`;
    } else {
        alertEro.className = "alert-card alert-success";
        msgEro.innerText = `Velocidad segura: ${v.toFixed(2)} m/s. Bajo los límites de desgaste de HDPE.`;
    }

    // Alerta 3: Resistencia de Presión Mecánica
    const alertPres = document.getElementById("alert-pressure");
    const msgPres = document.getElementById("alert-pres-msg");
    if (P_max_fondo > pn_limite) {
        alertPres.className = "alert-card alert-danger";
        msgPres.innerText = `FALLA MECÁNICA. P_máx fondo = ${P_max_fondo.toFixed(1)} bar supera la presión admisible PN = ${pn_limite} bar del SDR ${sdr}.`;
    } else if (P_max_fondo > pn_limite * 0.85) {
        alertPres.className = "alert-card alert-warning";
        msgPres.innerText = `Precaución. P_máx fondo = ${P_max_fondo.toFixed(1)} bar cerca al límite PN = ${pn_limite} bar. Margen estructural reducido.`;
    } else {
        alertPres.className = "alert-card alert-success";
        msgPres.innerText = `Estructuralmente seguro. P_máx fondo = ${P_max_fondo.toFixed(1)} bar bajo el límite PN = ${pn_limite} bar.`;
    }
}

// Pestañas (Tab Switcher)
function switchTab(tabId) {
    const contents = document.querySelectorAll(".tab-content");
    contents.forEach(content => content.classList.remove("active"));

    const buttons = document.querySelectorAll(".tab-btn");
    buttons.forEach(btn => btn.classList.remove("active"));

    document.getElementById(tabId).classList.add("active");
    event.currentTarget.classList.add("active");
}

// Acordeón Colapsable de Documentación
function toggleAccordion(id) {
    const el = document.getElementById(id);
    const arrow = document.getElementById("accordion-arrow");
    if (el.classList.contains("collapsed")) {
        el.classList.remove("collapsed");
        arrow.style.transform = "rotate(180deg)";
    } else {
        el.classList.add("collapsed");
        arrow.style.transform = "rotate(0deg)";
    }
}

/* ==========================================================================
   CONFIGURACIÓN DE GRÁFICOS INTERACTIVOS (CHART.JS)
   ========================================================================== */

// Gráfico 1: Perfil Longitudinal del Trazado
function inicializarGraficoPerfil() {
    const ctx = document.getElementById("chartProfile").getContext("2d");
    
    const labels = perfilDatos.map(p => p.abscisa);
    const terreno = perfilDatos.map(p => p.terreno);
    const clavePHD = perfilDatos.map(p => p.clavePHD);
    
    // Tubería superficial sigue al terreno a una distancia de 1.0 m
    const claveSup = perfilDatos.map((p, i) => {
        if (i === 0 || i === perfilDatos.length - 1) return p.clavePHD;
        return p.terreno - 1.0;
    });

    chartProfileInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Perfil del Terreno (Humedal)',
                    data: terreno,
                    borderColor: 'rgba(148, 163, 184, 0.5)',
                    backgroundColor: 'rgba(148, 163, 184, 0.05)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: true
                },
                {
                    label: 'Salmuera PHD Proyectada (Nueva)',
                    data: clavePHD,
                    borderColor: '#ef4444',
                    borderWidth: 3,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'Condensado PHD Proyectada (Nueva)',
                    data: clavePHD,
                    borderColor: '#10b981',
                    borderWidth: 3,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'Salmuera Superficial (Existente)',
                    data: claveSup,
                    borderColor: '#b91c1c',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'Condensado Superficial (Existente)',
                    data: claveSup,
                    borderColor: '#047857',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: true, text: 'Distancia Horizontal / Abscisas (m)', color: '#cbd5e1' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    title: { display: true, text: 'Elevación (m.s.n.m.)', color: '#cbd5e1' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#f8fafc', boxWidth: 20 }
                }
            }
        }
    });
}

// Gráfico 2: Perfil de Presiones a lo largo de las Abscisas
function actualizarGraficoPresiones(labels, presionesPHD, presionesSup, sdr) {
    const ctx = document.getElementById("chartPressure").getContext("2d");

    const limitesSDR = { 7.4: 25.0, 9: 20.0, 11: 16.0, 13.6: 12.5, 17: 10.0, 21: 8.0 };
    const pn_limite = limitesSDR[sdr];
    const limiteNominal = Array(labels.length).fill(pn_limite);

    if (chartPressureInstance) {
        chartPressureInstance.destroy();
    }

    chartPressureInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Presión en Trazado PHD (Enterrado)',
                    data: presionesPHD,
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.05)',
                    borderWidth: 3,
                    pointRadius: 2,
                    pointBackgroundColor: '#06b6d4',
                    fill: true
                },
                {
                    label: 'Presión en Trazado Superficial',
                    data: presionesSup,
                    borderColor: '#f59e0b',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: `Límite PN SDR ${sdr} (${pn_limite} bar)`,
                    data: limiteNominal,
                    borderColor: 'rgba(239, 68, 68, 0.7)',
                    borderWidth: 2,
                    borderDash: [6, 6],
                    pointRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: true, text: 'Abscisas del Trazado', color: '#cbd5e1' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    title: { display: true, text: 'Presión Interna (bar)', color: '#cbd5e1' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#f8fafc' }
                }
            }
        }
    });
}

// Gráfico 3: Curva de Pérdida vs Caudal
function actualizarGraficoPerdidas(ID, K_sup, K_phd, rho, mu) {
    const ctx = document.getElementById("chartLoss").getContext("2d");

    // Generar un rango de caudales de 10 a 200 L/s
    const caudales_lps = [];
    const dp_sup_curva = [];
    const dp_phd_curva = [];

    // Calcular longitudes totales
    let L_sup_total = 0;
    let L_phd_total = 0;

    for (let i = 1; i < perfilDatos.length; i++) {
        const punto = perfilDatos[i];
        const puntoAnt = perfilDatos[i - 1];
        
        let claveSup = punto.terreno - 1.0;
        if (i === perfilDatos.length - 1) claveSup = punto.clavePHD;
        let claveSupAnt = puntoAnt.terreno - 1.0;
        if (i - 1 === 0) claveSupAnt = puntoAnt.clavePHD;

        L_sup_total += Math.sqrt(Math.pow(punto.abscisa - puntoAnt.abscisa, 2) + Math.pow(claveSup - claveSupAnt, 2));
        L_phd_total += Math.sqrt(Math.pow(punto.abscisa - puntoAnt.abscisa, 2) + Math.pow(punto.clavePHD - puntoAnt.clavePHD, 2));
    }

    const roughnessRatio = RUGOSIDAD_HDPE / ID;

    for (let q_lps = 10; q_lps <= 220; q_lps += 10) {
        caudales_lps.push(q_lps);
        const Q = q_lps / 1000.0; // m^3/s
        const area = (Math.PI / 4.0) * Math.pow(ID, 2);
        const v = Q / area;

        const Re = (rho * v * ID) / mu;
        const f = calcularFriccionHaaland(Re, roughnessRatio);

        // Pérdida superficial
        const h_f_sup = f * (L_sup_total / ID) * (Math.pow(v, 2) / (2 * G));
        const h_m_sup = K_sup * (Math.pow(v, 2) / (2 * G));
        const dP_sup = (rho * G * (h_f_sup + h_m_sup)) / 1000.0; // kPa

        // Pérdida PHD
        const h_f_phd = f * (L_phd_total / ID) * (Math.pow(v, 2) / (2 * G));
        const h_m_phd = K_phd * (Math.pow(v, 2) / (2 * G));
        const dP_phd = (rho * G * (h_f_phd + h_m_phd)) / 1000.0; // kPa

        dp_sup_curva.push(dP_sup);
        dp_phd_curva.push(dP_phd);
    }

    if (chartLossInstance) {
        chartLossInstance.destroy();
    }

    chartLossInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: caudales_lps,
            datasets: [
                {
                    label: 'Pérdida Trazado PHD (Enterrado)',
                    data: dp_phd_curva,
                    borderColor: '#10b981',
                    borderWidth: 3,
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'Pérdida Trazado Superficial',
                    data: dp_sup_curva,
                    borderColor: '#f59e0b',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: true, text: 'Caudal Volumétrico (L/s)', color: '#cbd5e1' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    title: { display: true, text: 'Caída de Presión Dinámica (kPa)', color: '#cbd5e1' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#f8fafc' }
                }
            }
        }
    });
}
