document.addEventListener('DOMContentLoaded', () => {
    const modelSelect = document.getElementById('model-select');
    
    // UI Elements
    const fpsEl = document.getElementById('fps-val');
    const infTimeEl = document.getElementById('inf-time-val');
    const countEl = document.getElementById('count-val');
    const densityEl = document.getElementById('density-val');
    const audioVolEl = document.getElementById('audio-vol-val');
    const audioStateEl = document.getElementById('audio-state-val');
    const riskEl = document.getElementById('risk-val');

    // Handle Model Change
    modelSelect.addEventListener('change', async (e) => {
        const model = e.target.value;
        try {
            const res = await fetch('/api/set_model', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model })
            });
            const data = await res.json();
            console.log("Model changed to:", data.model);
        } catch (err) {
            console.error("Error changing model:", err);
        }
    });

    // Fetch Metrics periodically
    setInterval(async () => {
        try {
            const res = await fetch('/api/metrics');
            const data = await res.json();
            
            // Update Vision
            fpsEl.textContent = data.vision.fps;
            infTimeEl.textContent = data.vision.inference_time_ms + ' ms';
            countEl.textContent = data.vision.person_count;
            densityEl.textContent = data.vision.density;
            
            // Vision Colors
            densityEl.className = 'metric-value';
            if (data.vision.density === 'LOW') densityEl.classList.add('text-green');
            else if (data.vision.density === 'MEDIUM') densityEl.classList.add('text-yellow');
            else if (data.vision.density === 'HIGH') densityEl.classList.add('text-red');

            // Update Audio
            audioVolEl.textContent = data.audio.volume + '%';
            audioStateEl.textContent = data.audio.state;
            
            // Audio Colors
            audioStateEl.className = 'metric-value';
            if (data.audio.state === 'NORMAL') audioStateEl.classList.add('text-green');
            else if (data.audio.state === 'PANIC') audioStateEl.classList.add('text-red');

            // Update Risk
            riskEl.textContent = data.risk;
            riskEl.className = 'risk-value';
            if (data.risk === 'LOW') riskEl.classList.add('text-green');
            else if (data.risk === 'MEDIUM') riskEl.classList.add('text-yellow');
            else if (data.risk === 'HIGH') riskEl.classList.add('text-red');
            else if (data.risk === 'CRITICAL') {
                riskEl.classList.add('text-red');
                // Optional: Trigger loud browser alarm or UI flash here
            }
            
        } catch (err) {
            console.error("Error fetching metrics:", err);
        }
    }, 500); // Update every 500ms
});
