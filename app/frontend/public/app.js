const API_URL = '/.netlify/functions/api';

// Código de rastreamento que será fornecido aos usuários
const trackingCode = `<script>
(function() {
    fetch('${window.location.origin}${API_URL}/track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            page_url: window.location.href,
            referrer: document.referrer
        })
    });
})();
</script>`;

// Exibir código de rastreamento
document.getElementById('trackingCode').textContent = trackingCode;

// Função para copiar o código
function copyTrackingCode() {
    navigator.clipboard.writeText(trackingCode)
        .then(() => alert('Código copiado!'))
        .catch(err => console.error('Erro ao copiar:', err));
}

// Função para atualizar as estatísticas
async function updateStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        const stats = await response.json();

        // Atualizar visitas totais
        document.getElementById('totalVisits').textContent = stats.total_visits;

        // Atualizar navegadores
        const browsersDiv = document.getElementById('browsers');
        browsersDiv.innerHTML = Object.entries(stats.browsers)
            .map(([browser, count]) => `
                <div class="stat-item">
                    <span>${browser}</span>
                    <span>${count}</span>
                </div>
            `).join('');

        // Atualizar sistemas operacionais
        const osDiv = document.getElementById('os');
        osDiv.innerHTML = Object.entries(stats.operating_systems)
            .map(([os, count]) => `
                <div class="stat-item">
                    <span>${os}</span>
                    <span>${count}</span>
                </div>
            `).join('');

        // Atualizar dispositivos
        const devicesDiv = document.getElementById('devices');
        devicesDiv.innerHTML = Object.entries(stats.devices)
            .map(([device, count]) => `
                <div class="stat-item">
                    <span>${device}</span>
                    <span>${count}</span>
                </div>
            `).join('');

        // Atualizar países
        const countriesDiv = document.getElementById('countries');
        countriesDiv.innerHTML = Object.entries(stats.countries)
            .map(([country, count]) => `
                <div class="stat-item">
                    <span>${country}</span>
                    <span>${count}</span>
                </div>
            `).join('');

        // Atualizar visitas recentes
        const recentVisitsDiv = document.getElementById('recentVisits');
        recentVisitsDiv.innerHTML = stats.recent_visits
            .map(visit => `
                <div class="visit-item">
                    <p><strong>Data:</strong> ${new Date(visit.timestamp).toLocaleString()}</p>
                    <p><strong>Página:</strong> ${visit.page_url}</p>
                    <p><strong>Navegador:</strong> ${visit.browser} ${visit.browser_version}</p>
                    <p><strong>Sistema:</strong> ${visit.os} ${visit.os_version}</p>
                    <p><strong>Dispositivo:</strong> ${visit.device}</p>
                    <p><strong>Local:</strong> ${visit.geolocation.city}, ${visit.geolocation.country}</p>
                </div>
            `).join('');

    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Atualizar estatísticas a cada 30 segundos
updateStats();
setInterval(updateStats, 30000); 