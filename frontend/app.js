const API_URL = 'http://127.0.0.1:8000';
let network = null;
let availableItems = [];

// Initialize the application
async function init() {
    try {
        // Fetch base data to populate dropdowns
        const response = await fetch(`${API_URL}/data`);
        const data = await response.json();
        
        // Store items for dynamic rows
        availableItems = Object.entries(data.items).map(([key, val]) => ({
            key,
            name: val.name
        }));

        // Setup dynamic targets list
        const addTargetBtn = document.getElementById('addTargetBtn');
        addTargetBtn.addEventListener('click', () => {
            addTargetRow('eisen', 20);
            calculatePlan();
        });

        // Add a default row (Maisbot)
        addTargetRow('maisbot', 20);

        // Initialize empty network
        const container = document.getElementById('mynetwork');
        const options = {
            nodes: {
                shape: 'circularImage',
                font: { color: '#f8fafc', face: 'Outfit', size: 14, background: 'rgba(15, 23, 42, 0.6)' },
                color: {
                    background: 'rgba(30, 41, 59, 0.9)',
                    border: '#3b82f6',
                    highlight: { background: 'rgba(59, 130, 246, 0.8)', border: '#60a5fa' }
                },
                borderWidth: 2,
                size: 45,
                shadow: { enabled: true, color: 'rgba(0,0,0,0.5)', size: 10, x: 0, y: 5 }
            },
            edges: {
                width: 3,
                color: { color: '#475569', highlight: '#3b82f6' },
                font: { color: '#94a3b8', strokeWidth: 2, strokeColor: '#0f172a', align: 'middle', size: 12 },
                arrows: { to: { enabled: true, scaleFactor: 1 } },
                smooth: { type: 'cubicBezier', forceDirection: 'horizontal', roundness: 0.6 }
            },
            layout: {
                hierarchical: {
                    direction: 'LR', // Left to Right flow!
                    sortMethod: 'directed',
                    nodeSpacing: 180, // Increased spacing to prevent overlapping
                    levelSeparation: 320, // Increased separation
                    edgeMinimization: true,
                    parentCentralization: true
                }
            },
            physics: false
        };
        network = new vis.Network(container, { nodes: new vis.DataSet([]), edges: new vis.DataSet([]) }, options);

        // Bind settings change events
        document.getElementById('assemblerLevel').addEventListener('change', calculatePlan);
        document.getElementById('smelterLevel').addEventListener('change', calculatePlan);
        document.getElementById('crusherLevel').addEventListener('change', calculatePlan);
        document.getElementById('minerLevel').addEventListener('change', calculatePlan);
        document.getElementById('purityLevel').addEventListener('change', calculatePlan);
        document.getElementById('calculateBtn').addEventListener('click', calculatePlan);
        
        // Initial calculation
        calculatePlan();

    } catch (error) {
        console.error("Error initializing data:", error);
    }
}

function addTargetRow(selectedItem = '', rate = 20) {
    const list = document.getElementById('targetsList');
    const row = document.createElement('div');
    row.className = 'target-row';
    
    const select = document.createElement('select');
    availableItems.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item.key;
        opt.textContent = item.name;
        if (item.key === selectedItem) opt.selected = true;
        select.appendChild(opt);
    });
    
    const input = document.createElement('input');
    input.type = 'number';
    input.value = rate;
    input.min = 1;
    
    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-btn';
    removeBtn.textContent = '×';
    removeBtn.onclick = () => {
        row.remove();
        calculatePlan();
    };
    
    row.appendChild(select);
    row.appendChild(input);
    row.appendChild(removeBtn);
    list.appendChild(row);
    
    select.addEventListener('change', calculatePlan);
    input.addEventListener('input', calculatePlan);
}

async function calculatePlan() {
    const targets = [];
    document.querySelectorAll('.target-row').forEach(row => {
        const item = row.querySelector('select').value;
        const rate = parseFloat(row.querySelector('input').value) || 0;
        if (rate > 0) {
            targets.push({ item, rate });
        }
    });

    if (targets.length === 0) {
        network.setData({ nodes: new vis.DataSet([]), edges: new vis.DataSet([]) });
        return;
    }

    const settings = {
        assemblerLevel: document.getElementById('assemblerLevel').value,
        smelterLevel: document.getElementById('smelterLevel').value,
        crusherLevel: document.getElementById('crusherLevel').value,
        minerLevel: document.getElementById('minerLevel').value,
        purity: document.getElementById('purityLevel').value,
        beltLevel: '1'
    };

    const reqBody = { targets, settings };

    try {
        const btn = document.getElementById('calculateBtn');
        btn.textContent = "Berechne...";
        
        const response = await fetch(`${API_URL}/calculate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reqBody)
        });
        
        const graphData = await response.json();
        
        // Transform data for Vis.js
        const visNodes = new vis.DataSet(graphData.nodes.map(n => {
            const nodeObj = {
                id: n.id,
                label: n.label, // Label will be empty for normal nodes, text for output nodes
                title: n.title // Tooltip on hover
            };
            
            if (n.image) {
                nodeObj.shape = 'circularImage';
                nodeObj.image = n.image;
                
                // Style output nodes differently (green border)
                if (n.isOutput) {
                    nodeObj.color = {
                        border: '#10b981',
                        background: 'rgba(16, 185, 129, 0.2)',
                        highlight: { border: '#34d399', background: 'rgba(16, 185, 129, 0.4)' }
                    };
                    nodeObj.borderWidth = 3;
                }
            } else {
                nodeObj.shape = 'box';
            }
            
            return nodeObj;
        }));
        
        const visEdges = new vis.DataSet(graphData.edges.map(e => ({
            id: e.id,
            from: e.from,
            to: e.to,
            label: e.label
        })));

        network.setData({ nodes: visNodes, edges: visEdges });
        
        btn.textContent = "Plan Berechnen";

    } catch (error) {
        console.error("Error calculating plan:", error);
        document.getElementById('calculateBtn').textContent = "Fehler!";
        setTimeout(() => document.getElementById('calculateBtn').textContent = "Plan Berechnen", 2000);
    }
}

document.addEventListener('DOMContentLoaded', init);
