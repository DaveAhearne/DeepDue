let selectedEntities = new Set();
let timer = null;
let startTime = null;

const NODE_LABELS = {
    init: 'init',
    route_extraction_by_type: 'route',
    get_company: 'company_lookup',
    officer_extraction: 'officer_extraction',
    filing_history: 'filing_history',
    pscs_extraction: 'psc_extraction',
    enqueue_company: 'enqueue_company',
    get_officer_appointments: 'officer_appointments',
    enqueue_officer: 'enqueue_officer',
    should_continue: 'should_continue',
    dequeue_next: 'dequeue_next',
    pattern_detection: 'pattern_detection',
};

// Start timer when SSE connection opens
document.addEventListener('htmx:sseOpen', () => {
    startTime = Date.now();
    timer = setInterval(() => {
        const el = document.getElementById('log-meta');
        if (el) el.textContent = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
    }, 100);
});

// Stop timer when SSE connection closes
document.addEventListener('htmx:sseClose', () => {
    clearInterval(timer);
    timer = null;
});

// Reset state when a new investigation is submitted
document.addEventListener('htmx:beforeRequest', () => {
    selectedEntities.clear();
    updateInvestigateButton();
});

// Multi-select via event delegation (flags panel is dynamically swapped in)
document.addEventListener('click', e => {
    const card = e.target.closest('.flag-card');
    if (!card) return;

    const entities = (card.dataset.entities || '').split(',').filter(Boolean);

    if (card.classList.contains('selected')) {
        card.classList.remove('selected');
        entities.forEach(id => selectedEntities.delete(id));
    } else {
        card.classList.add('selected');
        entities.forEach(id => selectedEntities.add(id));
    }

    updateInvestigateButton();
});

function updateInvestigateButton() {
    const btn = document.getElementById('btn-investigate');
    if (!btn) return;
    if (selectedEntities.size > 0) {
        btn.classList.add('visible');
        btn.textContent = `Investigate selected (${selectedEntities.size})`;
    } else {
        btn.classList.remove('visible');
    }
}

function toggleMenu() {
    document.getElementById('hamburger').classList.toggle('open');
    document.getElementById('mobile-menu').classList.toggle('open');
}