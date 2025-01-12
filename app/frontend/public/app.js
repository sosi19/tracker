const API_URL = '/api';

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

// Função para copiar o código
function copyTrackingCode() {
    navigator.clipboard.writeText(trackingCode)
        .then(() => alert('Código copiado!'))
        .catch(err => console.error('Erro ao copiar:', err));
}

async function createTrackingLink() {
    const targetUrl = document.getElementById('targetUrl').value;
    
    try {
        const response = await fetch(`${API_URL}/create-link`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ target_url: targetUrl })
        });

        console.log('Status:', response.status);
        const responseText = await response.text();
        console.log('Response:', responseText);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Erro ao fazer parse do JSON:', responseText);
            throw new Error(`Resposta inválida do servidor. Status: ${response.status}`);
        }
        
        if (data.success) {
            const linkResult = document.getElementById('linkResult');
            const trackingLink = document.getElementById('trackingLink');
            
            linkResult.style.display = 'block';
            trackingLink.value = data.tracking_link;
        } else {
            alert('Erro ao criar o link: ' + (data.error || 'Erro desconhecido'));
        }
    } catch (error) {
        console.error('Erro completo:', error);
        alert('Erro ao criar o link: ' + error.message);
    }
}

function copyTrackingLink() {
    const trackingLink = document.getElementById('trackingLink');
    trackingLink.select();
    document.execCommand('copy');
    alert('Link copiado para a área de transferência!');
}

// Função para testar a API
async function testAPI() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);

        const response = await fetch(`${API_URL}/test`, {
            signal: controller.signal,
            headers: {
                'Accept': 'application/json'
            }
        });
        clearTimeout(timeoutId);

        if (!response.ok) {
            const text = await response.text();
            console.error('Resposta da API:', text);
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Teste API:', data);
        alert(data.message || 'API respondeu com sucesso!');
    } catch (error) {
        console.error('Erro completo:', error);
        if (error.name === 'AbortError') {
            alert('Timeout: A API demorou muito para responder');
        } else {
            alert('Erro ao testar API: ' + error.message);
        }
    }
}

// Função para testar a conexão com o banco
async function testDB() {
    try {
        const response = await fetch(`${API_URL}/test-db`, {
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const text = await response.text();
            console.error('Resposta do teste DB:', text);
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Teste DB:', data);
        alert(data.message || 'Conexão com banco estabelecida!');
    } catch (error) {
        console.error('Erro completo:', error);
        alert('Erro ao testar banco: ' + error.message);
    }
} 