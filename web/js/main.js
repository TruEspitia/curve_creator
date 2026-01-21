// Main Logic

let currentTab = 'predefined';
let allFunctions = []; // Store all functions to allow filtering

async function init() {
    console.log("Initializing App...");

    // 1. Notify Backend
    let status = await eel.app_ready()();
    console.log(status);

    // 2. Load Function List
    await refreshFunctions();

    // 3. Setup Listeners
    setupListeners();

    // 4. Initial Plot
    initPlot();
}

function initPlot() {
    const layout = {
        title: 'Data Preview',
        paper_bgcolor: '#1e1e1e',
        plot_bgcolor: '#1e1e1e',
        font: { color: '#d4d4d4' },
        xaxis: { gridcolor: '#444' },
        yaxis: { gridcolor: '#444' },
        margin: { t: 40, r: 20, b: 40, l: 40 }
    };

    Plotly.newPlot('plot-container', [], layout, { responsive: true });
}

function setupListeners() {
    // File Load
    document.getElementById('btn-load-data').addEventListener('click', async () => {
        let filePath = await eel.pick_file()();
        if (filePath) {
            document.getElementById('data-file-info').innerText = "Loading...";
            let result = await eel.load_data_file(filePath)();

            if (result.error) {
                alert("Error: " + result.error);
                document.getElementById('data-file-info').innerText = "Error loading file";
            } else {
                document.getElementById('data-file-info').innerText = result.filename;
                populateColumnSelectors(result.columns);
                plotData(result, result.columns[0], result.columns[1]);
                enableControls();
            }
        }
    });

    // Column Selectors
    document.getElementById('select-x-col').addEventListener('change', updatePlotFromSelection);
    document.getElementById('select-y-col').addEventListener('change', updatePlotFromSelection);

    // Engine Selection - Filter functions
    document.getElementById('select-engine').addEventListener('change', filterFunctions);

    // Tab Switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const tab = btn.dataset.tab;
            currentTab = tab;

            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            document.getElementById(`tab-${tab}`).style.display = 'block';
        });
    });

    // Perform Fit
    document.getElementById('btn-fit').addEventListener('click', async () => {
        const colX = document.getElementById('select-x-col').value;
        const colY = document.getElementById('select-y-col').value;
        const engine = document.getElementById('select-engine').value;

        let result;

        // Show Blocking Modal
        const modal = document.getElementById('progress-modal');
        const progressText = document.getElementById('progress-text');

        modal.style.display = 'flex';
        progressText.innerText = `Optimization in progress (${engine})...`;

        // Use a small timeout to allow UI to render modal before blocking call
        setTimeout(async () => {
            try {
                if (currentTab === 'predefined') {
                    const funcName = document.getElementById('select-function').value;
                    if (!funcName) {
                        alert("Please select a function from the library.");
                        modal.style.display = 'none';
                        return;
                    }
                    result = await eel.run_fit(funcName, colX, colY, engine)();
                } else {
                    const formula = document.getElementById('custom-formula').value;
                    const params = document.getElementById('custom-params').value;
                    if (!formula) {
                        alert("Please enter a formula.");
                        modal.style.display = 'none';
                        return;
                    }
                    result = await eel.run_custom_fit(formula, params, colX, colY)();
                }

                console.log("Fit result:", result);

                if (result.success) {
                    displayResults(result);
                    plotFit(result, colX, colY);
                } else {
                    alert("Fit Failed: " + result.error);
                }
            } catch (e) {
                alert("An error occurred: " + e);
            } finally {
                // Hide Modal
                modal.style.display = 'none';
            }
        }, 100);
    });
}

function populateColumnSelectors(columns) {
    let selX = document.getElementById('select-x-col');
    let selY = document.getElementById('select-y-col');
    let container = document.getElementById('column-selectors');

    selX.innerHTML = '';
    selY.innerHTML = '';

    columns.forEach(col => {
        let optX = document.createElement('option');
        optX.value = col;
        optX.innerText = col;
        selX.appendChild(optX);

        let optY = document.createElement('option');
        optY.value = col;
        optY.innerText = col;
        selY.appendChild(optY);
    });

    if (columns.length >= 2) {
        selX.value = columns[0];
        selY.value = columns[1];
    }

    container.style.display = 'block';
}

function updatePlotFromSelection() {
    if (!storedData) return;
    let colX = document.getElementById('select-x-col').value;
    let colY = document.getElementById('select-y-col').value;
    plotData(storedData, colX, colY);
}

async function refreshFunctions() {
    allFunctions = await eel.get_functions_list()();
    filterFunctions();
}

function filterFunctions() {
    const engine = document.getElementById('select-engine').value;
    const select = document.getElementById('select-function');
    select.innerHTML = '<option value="" disabled selected>Select Function...</option>';

    // Determine max complexity allowed
    // LM: 1
    // DE: 1, 2
    // Sequential: 1, 2, 3
    let maxComplexity = 3;
    if (engine === 'lm') maxComplexity = 1;
    else if (engine === 'de') maxComplexity = 2;
    else maxComplexity = 3;

    let visibleCount = 0;
    allFunctions.forEach(f => {
        // Default to 1 if not present
        let complexity = (f.metadata && f.metadata.complexity) ? parseInt(f.metadata.complexity) : 1;

        if (complexity <= maxComplexity) {
            let opt = document.createElement('option');
            opt.value = f.name;
            opt.innerText = f.name;
            select.appendChild(opt);
            visibleCount++;
        }
    });

    console.log(`Engine: ${engine}, MaxComplexity: ${maxComplexity}, Visible: ${visibleCount}`);
}

function enableControls() {
    document.getElementById('btn-fit').disabled = false;
}

let storedData = null; // Keep copy for plotting

function plotData(dataObj, colX, colY) {
    storedData = dataObj;

    let x = dataObj.data.map(d => d[colX]);
    let y = dataObj.data.map(d => d[colY]);

    let trace = {
        x: x,
        y: y,
        mode: 'markers',
        type: 'scatter',
        name: 'Data',
        marker: { color: '#007acc' }
    };

    let layout = document.getElementById('plot-container').layout;
    layout.xaxis = { title: { text: colX }, gridcolor: '#444' };
    layout.yaxis = { title: { text: colY }, gridcolor: '#444' };

    Plotly.react('plot-container', [trace], layout);
}

function plotFit(fitResult, colX, colY) {
    if (!storedData) return;

    let x = storedData.data.map(d => d[colX]);
    let y_fit = fitResult.fitted_curve;

    let combined = x.map((val, idx) => ({ x: val, y: y_fit[idx] }));
    combined.sort((a, b) => a.x - b.x);

    let traceData = {
        x: x,
        y: storedData.data.map(d => d[colY]),
        mode: 'markers',
        type: 'scatter',
        name: 'Data',
        marker: { color: '#007acc' }
    };

    let traceFit = {
        x: combined.map(c => c.x),
        y: combined.map(c => c.y),
        mode: 'lines',
        type: 'scatter',
        name: 'Fit',
        line: { color: '#4caf50', width: 3 }
    };

    Plotly.react('plot-container', [traceData, traceFit], document.getElementById('plot-container').layout);
}

function displayResults(result) {
    let container = document.getElementById('fit-results');
    let html = `<div><strong>Method:</strong> ${result.engine || "Unknown"}</div>`;
    html += `<div><strong>R²:</strong> ${result.r_squared.toFixed(4)}</div>`;
    html += `<div><strong>RMSE:</strong> ${result.rmse ? result.rmse.toFixed(5) : "N/A"}</div>`;
    html += `<hr/>`;

    for (let [key, val] of Object.entries(result.parameters)) {
        let err = result.errors[key] || 0;
        let errPercent = Math.abs(err / val * 100);
        html += `<div><strong>${key}:</strong> ${val.toExponential(3)} ± ${err.toExponential(2)} (${errPercent.toFixed(1)}%)</div>`;
    }

    container.innerHTML = html;
}

// Start
init();
