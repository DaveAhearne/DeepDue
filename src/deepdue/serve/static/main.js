let startTime;

async function runInvestigation() {
    const input = document.getElementById('company-input').value.trim();
    if (!input) return;

    const btn = document.getElementById('run-btn');
    const panel = document.getElementById('result-panel');
    const dot = document.getElementById('result-dot');
    const label = document.getElementById('result-label');
    const meta = document.getElementById('result-meta');
    const body = document.getElementById('result-body');
    const stats = document.getElementById('stats-row');

    btn.disabled = true;
    panel.classList.add('visible');
    stats.classList.remove('visible');
    dot.className = 'result-dot running';
    label.textContent = 'Investigating — ' + input;
    body.className = 'result-body';
    body.textContent = '';
    startTime = Date.now();

    const timer = setInterval(() => {
        meta.textContent = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
    }, 100);

    try {
        const res = await fetch('/investigation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ company_number: input })
        });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail ?? `Server returned ${res.status}`);
        }

        const data = await res.json();
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

        dot.className = 'result-dot done';
        label.textContent = 'Complete — ' + input;
        body.textContent = JSON.stringify(data, null, 2);

        document.getElementById('stat-entities').textContent = data.entities_visited?.length ?? '—';
        document.getElementById('stat-flags').textContent = data.flags?.length ?? '—';
        document.getElementById('stat-calls').textContent = data.api_calls ?? '—';
        document.getElementById('stat-duration').textContent = elapsed + 's';
        stats.classList.add('visible');

    } catch (err) {
        dot.className = 'result-dot error';
        label.textContent = 'Error';
        body.className = 'result-body error';
        body.textContent = err.message;
    } finally {
        clearInterval(timer);
        btn.disabled = false;
    }
}

document.getElementById('company-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') runInvestigation();
});

function toggleMenu() {
    const btn = document.getElementById('hamburger');
    const menu = document.getElementById('mobile-menu');
    btn.classList.toggle('open');
    menu.classList.toggle('open');
}