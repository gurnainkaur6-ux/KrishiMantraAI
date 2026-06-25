/**
 * KrishiMitra AI - Decision Support Dashboard Logic
 */

// Memory Fields Definition
const FIELDS = ['state', 'district', 'soil_type', 'crop', 'temperature', 'humidity', 'rainfall'];

// Unsafe keywords to inspect
const UNSAFE_KEYWORDS = [
    'double dose',
    '10x',
    'excessive pesticide',
    'kill faster',
    'overdose',
    'maximum chemical'
];

// Offline expert knowledge base
const KNOWLEDGE_BASE = {
    "wheat": {
        "crop2": "Maize",
        "organic": "Well-decomposed Farmyard Manure (FYM) or compost at 4-6 tonnes/acre",
        "npk": "120 kg Urea, 55 kg DAP, and 10 kg MOP per acre (adjust based on soil test report)",
        "pesticide": "Propiconazole 25% EC at 200 ml/acre diluted in 200 liters of water (for stripe/yellow rust)",
        "waiting_period": "30 days between final spray and harvest",
        "ppe": "Wear nitrile/chemical-resistant gloves, protective goggles, long pants, a long-sleeved shirt, and boots. Spray in the direction of the wind.",
        "temp_range": [15, 22],
        "rust_risk_humidity": 60
    },
    "rice": {
        "crop2": "Wheat",
        "organic": "Green manuring (dhaincha) or well-decomposed FYM at 6 tonnes/acre",
        "npk": "110 kg Urea, 30 kg DAP, and 20 kg MOP per acre",
        "pesticide": "Tricyclazole 75% WP @ 120 g/acre in 200L water (for blast control) or Streptocycline @ 6 g/acre (BLB)",
        "waiting_period": "28 days",
        "ppe": "Wear protective face shield, rubber gloves, apron, and boots. Do not spray during heavy rains.",
        "temp_range": [22, 35],
        "rust_risk_humidity": 75
    },
    "cotton": {
        "crop2": "Pigeonpea or Soybean",
        "organic": "Compost or Farmyard Manure @ 5 tonnes/acre",
        "npk": "100 kg Urea, 75 kg Single Super Phosphate (SSP), and 30 kg MOP per acre",
        "pesticide": "Spinosad 45% SC @ 60 ml/acre in 200L water (for Bollworm control)",
        "waiting_period": "30 days",
        "ppe": "Wear heavy-duty gloves, protective respirator mask, goggles, and long-sleeved clothing.",
        "temp_range": [20, 32],
        "rust_risk_humidity": 70
    },
    "maize": {
        "crop2": "Finger Millet / Ragi",
        "organic": "FYM or compost @ 4 tonnes/acre",
        "npk": "150 kg Urea, 60 kg DAP, and 30 kg MOP per acre",
        "pesticide": "Chlorantraniliprole 18.5% SC @ 80 ml/acre in 200L water (for Fall Armyworm)",
        "waiting_period": "30 days",
        "ppe": "Wear chemical-resistant gloves, face mask, protective safety glasses, and full body clothing.",
        "temp_range": [18, 30],
        "rust_risk_humidity": 70
    },
    "sugarcane": {
        "crop2": "Mustard or Potato (as intercrops in autumn sowing)",
        "organic": "Pressmud or Farmyard Manure @ 10 tonnes/acre",
        "npk": "120 kg Urea, 80 kg DAP, and 40 kg MOP per acre",
        "pesticide": "Imidacloprid 17.8% SL @ 100 ml/acre in 200L water (for early shoot borer)",
        "waiting_period": "45 days",
        "ppe": "Wear chemical-resistant boots, apron, goggles, and nitrile gloves. Avoid spray drift.",
        "temp_range": [20, 35],
        "rust_risk_humidity": 75
    },
    "groundnut": {
        "crop2": "Pearl Millet or Sesame",
        "organic": "Farmyard Manure @ 4 tonnes/acre",
        "npk": "25 kg Urea, 50 kg DAP, and 20 kg MOP per acre (Apply Gypsum @ 100-150 kg/acre at flowering)",
        "pesticide": "Mancozeb 75% WP @ 400 g/acre in 200L water (for Tikka Leaf Spot control)",
        "waiting_period": "21 days",
        "ppe": "Wear dust mask during mixing, protective gloves, goggles, and long-sleeved clothing.",
        "temp_range": [22, 30],
        "rust_risk_humidity": 65
    },
    "bajra (pearl millet)": {
        "crop2": "Moth Bean or Cluster Bean",
        "organic": "Farmyard Manure @ 2-3 tonnes/acre",
        "npk": "40 kg Urea and 30 kg DAP per acre",
        "pesticide": "Mancozeb 75% WP @ 400 g/acre in 200L water (for Downy Mildew control)",
        "waiting_period": "21 days",
        "ppe": "Use protective face mask, safety glasses, gloves, and protective clothing.",
        "temp_range": [25, 38],
        "rust_risk_humidity": 50
    },
    "tea": {
        "crop2": "Shade trees (Albizia lebbeck / Indigofera teysmannii)",
        "organic": "Neem cake or well-composted organic mulch @ 2 tonnes/acre",
        "npk": "Standard NPK 2:1:2 mixture (~60 kg Nitrogen/acre/year in split applications)",
        "pesticide": "Propargite 57% EC @ 200 ml/acre in 200L water (for Red Spider Mites)",
        "waiting_period": "7-14 days",
        "ppe": "Wear complete PPE (chemical apron, rubber gloves, goggles, and face mask). Spray when bushes are dry.",
        "temp_range": [18, 30],
        "rust_risk_humidity": 80
    }
};

// State Variables
let currentMemory = {};
let geminiApiKey = "";

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadMemory();
    setupEventListeners();
    updateApiBadge();
});

// Load variables from localStorage
function loadMemory() {
    FIELDS.forEach(field => {
        const val = localStorage.getItem(`km_${field}`);
        if (val !== null) {
            currentMemory[field] = val;
            
            // Populate form input elements
            const inputEl = document.getElementById(field);
            if (inputEl) {
                inputEl.value = val;
            }
            
            // Populate sidebar list
            const displayEl = document.getElementById(`m-${field}`);
            if (displayEl) {
                displayEl.textContent = val;
                displayEl.classList.remove('empty');
            }
        }
    });

    geminiApiKey = localStorage.getItem('km_gemini_api_key') || "";
    document.getElementById('api-key-input').value = geminiApiKey;
}

// Setup Dashboard Interactions
function setupEventListeners() {
    // Form Submit
    document.getElementById('parameters-form').addEventListener('submit', handleFormSubmit);

    // Clear Memory
    document.getElementById('clear-memory-btn').addEventListener('click', clearMemory);

    // Modal Events
    const settingsModal = document.getElementById('settings-modal');
    document.getElementById('open-settings-btn').addEventListener('click', () => {
        settingsModal.classList.remove('hidden');
    });
    document.getElementById('close-settings-btn').addEventListener('click', () => {
        settingsModal.classList.add('hidden');
    });
    document.getElementById('save-settings-btn').addEventListener('click', saveSettings);

    // Toggle Key Visibility
    document.getElementById('toggle-key-visibility').addEventListener('click', () => {
        const input = document.getElementById('api-key-input');
        const icon = document.querySelector('#toggle-key-visibility i');
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    });
}

// Update UI badge based on key presence
function updateApiBadge() {
    const badge = document.getElementById('api-status');
    const indicator = badge.querySelector('.status-indicator');
    const text = badge.querySelector('.status-text');
    
    if (geminiApiKey) {
        indicator.className = "status-indicator online";
        text.textContent = "Gemini Live Agents Active";
    } else {
        indicator.className = "status-indicator offline";
        text.textContent = "Offline Mode (Rule-Based)";
    }
}

// Clear local memory
function clearMemory() {
    FIELDS.forEach(field => {
        localStorage.removeItem(`km_${field}`);
        currentMemory[field] = null;
        
        const inputEl = document.getElementById(field);
        if (inputEl) inputEl.value = "";
        
        const displayEl = document.getElementById(`m-${field}`);
        if (displayEl) {
            displayEl.textContent = "Not Set";
            displayEl.classList.add('empty');
        }
    });
    
    // Clear outputs
    resetOutputs();
}

function resetOutputs() {
    document.getElementById('security-alert').classList.add('hidden');
    document.getElementById('report-output').classList.remove('hidden');
    
    ['r-crop1', 'r-crop2', 'r-organic', 'r-npk', 'r-irrigation', 'r-alert', 'r-dosage', 'r-waiting_period', 'r-safety'].forEach(id => {
        document.getElementById(id).textContent = "-";
    });
    
    document.getElementById('r-final_recommendation').innerHTML = '<p class="placeholder-text">Please submit the parameters form to generate final checklists.</p>';
}

// Save API key
function saveSettings() {
    const key = document.getElementById('api-key-input').value.trim();
    localStorage.setItem('km_gemini_api_key', key);
    geminiApiKey = key;
    updateApiBadge();
    document.getElementById('settings-modal').classList.add('hidden');
}

// Inspect inputs for security guardrails
function inspectSafety(inputs) {
    for (const val of Object.values(inputs)) {
        if (val) {
            const valLower = String(val).toLowerCase();
            for (const kw of UNSAFE_KEYWORDS) {
                if (valLower.includes(kw)) {
                    return false; // Violation detected
                }
            }
        }
    }
    return true; // Safe
}

// Submit Form Handler
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Get form inputs
    const inputs = {
        state: document.getElementById('state').value.trim(),
        district: document.getElementById('district').value.trim(),
        soil_type: document.getElementById('soil_type').value,
        crop: document.getElementById('crop').value,
        temperature: parseFloat(document.getElementById('temperature').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        rainfall: parseFloat(document.getElementById('rainfall').value),
        safety_notes: document.getElementById('safety_notes').value.trim()
    };

    // Run security guardrail check
    if (!inspectSafety(inputs)) {
        document.getElementById('report-output').classList.add('hidden');
        document.getElementById('security-alert').classList.remove('hidden');
        return;
    }

    // Hide alert if clean
    document.getElementById('security-alert').classList.add('hidden');
    document.getElementById('report-output').classList.remove('hidden');

    // Update context memory
    FIELDS.forEach(field => {
        localStorage.setItem(`km_${field}`, inputs[field]);
        currentMemory[field] = inputs[field];
        
        const displayEl = document.getElementById(`m-${field}`);
        if (displayEl) {
            displayEl.textContent = inputs[field];
            displayEl.classList.remove('empty');
        }
    });

    // Run Decision generation
    let results = null;
    if (geminiApiKey) {
        results = await generateGeminiRecommendations(inputs);
    }
    
    // Fall back if Gemini fails or is disabled
    if (!results) {
        results = generateLocalRecommendations(inputs);
    }

    // Populate UI
    renderReports(results);
}

// Offline rule-based execution
function generateLocalRecommendations(inputs) {
    let cropKey = inputs.crop.toLowerCase().trim();
    if (cropKey.includes("bajra") || cropKey.includes("millet")) {
        cropKey = "bajra (pearl millet)";
    }

    const info = KNOWLEDGE_BASE[cropKey] || {
        crop2: "Pulses / Legumes",
        organic: "General compost or vermicompost @ 4 tonnes/acre",
        npk: "Soil test directed general NPK fertilization",
        pesticide: "Use bio-pesticides (like neem oil 1500 ppm @ 1L/acre)",
        waiting_period: "Refer to local pesticide label safety instructions",
        ppe: "Wear safety gloves, eye goggles, protective mask, long-sleeved clothes, and shoes.",
        temp_range: [20, 30],
        rust_risk_humidity: 70
    };

    // Irrigation
    let irrigation = "";
    if (inputs.rainfall > 100) {
        irrigation = `Suspend irrigation. Heavy rainfall (${inputs.rainfall} mm) is more than sufficient. Clear drainage channels to prevent waterlogging.`;
    } else if (inputs.rainfall > 30) {
        irrigation = `Delay irrigation due to moderate/heavy rainfall (${inputs.rainfall} mm). Monitor crop needs.`;
    } else if (inputs.rainfall > 10) {
        irrigation = `Delay/reduce scheduled irrigation. Recent rainfall of ${inputs.rainfall} mm provides partial soil moisture.`;
    } else {
        irrigation = `Irrigate as per routine scheduling. Dry conditions (${inputs.rainfall} mm rainfall) require regular monitoring of soil moisture.`;
    }

    // Alerts
    const alerts = [];
    if (info.temp_range) {
        const [minOpt, maxOpt] = info.temp_range;
        if (inputs.temperature > maxOpt) {
            alerts.push(`High temperature of ${inputs.temperature}°C exceeds the optimal range (${minOpt}-${maxOpt}°C), which may cause heat stress.`);
        } else if (inputs.temperature < minOpt) {
            alerts.push(`Low temperature of ${inputs.temperature}°C is below optimal (${minOpt}-${maxOpt}°C), which might delay crop growth.`);
        }
    }
    if (inputs.humidity >= info.rust_risk_humidity) {
        alerts.push(`Relative humidity is high (${inputs.humidity}%), creating optimal conditions for fungal/disease outbreaks (e.g., rusts, mildews, or blights).`);
    }
    if (alerts.length === 0) {
        alerts.push("No critical weather risk alerts at this time. Maintain routine monitoring.");
    }

    return {
        soil: {
            crop1: `${inputs.crop} (Highly suitable for ${inputs.soil_type} soil in ${inputs.district}, ${inputs.state})`,
            crop2: info.crop2,
            organic: info.organic,
            npk: info.npk
        },
        weather: {
            irrigation: irrigation,
            alert: alerts.join(" ")
        },
        pesticide: {
            dosage: info.pesticide,
            waiting_period: info.waiting_period,
            safety: info.ppe
        }
    };
}

// Fetch recommendations using Gemini API
async function generateGeminiRecommendations(inputs) {
    const prompt = `
    You are KrishiMitra AI, an Indian Agriculture Multi-Agent Decision Support System. Given the following inputs:
    State: ${inputs.state}
    District: ${inputs.district}
    Soil Type: ${inputs.soil_type}
    Crop: ${inputs.crop}
    Temperature: ${inputs.temperature}°C
    Humidity: ${inputs.humidity}%
    Rainfall: ${inputs.rainfall}mm
    Special Notes: ${inputs.safety_notes}

    Generate specific agricultural recommendation reports for Soil, Weather, and Pesticide Safety.
    
    You MUST respond with a JSON object containing EXACTLY this structure:
    {
      "soil": {
        "crop1": "Suitability comment of primary crop",
        "crop2": "Recommended rotation/alternative crop",
        "organic": "Organic fertilizer details",
        "npk": "NPK chemical fertilizer dosage per acre"
      },
      "weather": {
        "irrigation": "Irrigation actions considering rainfall",
        "alert": "Temperature/humidity stress or disease alerts"
      },
      "pesticide": {
        "dosage": "Specific safe chemical dosage",
        "waiting_period": "Safety waiting interval before harvest",
        "safety": "Required personal protective equipment"
      }
    }
    `;

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${geminiApiKey}`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{ parts: [{ text: prompt }] }],
                generationConfig: {
                    responseMimeType: "application/json"
                }
            })
        });

        if (!response.ok) throw new Error("API call failed");

        const data = await response.json();
        const responseText = data.candidates[0].content.parts[0].text;
        return JSON.parse(responseText.trim ? responseText.trim() : responseText);
    } catch (e) {
        console.warn("Gemini API call failed, falling back to local engine:", e);
        return null;
    }
}

// Render recommendations in the browser
function renderReports(results) {
    // Soil
    document.getElementById('r-crop1').textContent = results.soil.crop1;
    document.getElementById('r-crop2').textContent = results.soil.crop2;
    document.getElementById('r-organic').textContent = results.soil.organic;
    document.getElementById('r-npk').textContent = results.soil.npk;

    // Weather
    document.getElementById('r-irrigation').textContent = results.weather.irrigation;
    document.getElementById('r-alert').textContent = results.weather.alert;

    // Pesticide
    document.getElementById('r-dosage').textContent = results.pesticide.dosage;
    document.getElementById('r-waiting_period').textContent = results.pesticide.waiting_period;
    document.getElementById('r-safety').textContent = results.pesticide.safety;

    // Final checklist actions (GitHub oriented action lists)
    const checklistHtml = `
        <div class="recommendation-list">
            <div class="recommendation-item">
                <input type="checkbox" id="chk-1">
                <label for="chk-1">Monitor crop growth relative to potential temperature/disease warnings.</label>
            </div>
            <div class="recommendation-item">
                <input type="checkbox" id="chk-2">
                <label for="chk-2">Execute irrigation: ${results.weather.irrigation.split('.')[0]}.</label>
            </div>
            <div class="recommendation-item">
                <input type="checkbox" id="chk-3">
                <label for="chk-3">Confirm PPE compliance: <em>${results.pesticide.safety.toLowerCase()}</em> before applying treatments.</label>
            </div>
        </div>
    `;
    document.getElementById('r-final_recommendation').innerHTML = checklistHtml;
}
