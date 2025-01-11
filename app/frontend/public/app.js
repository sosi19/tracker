const API_URL = '/.netlify/functions/api';

async function createLink(event) {
    event.preventDefault();
    
    const targetUrl = document.getElementById('targetUrl').value;
    const description = document.getElementById('description').value;
    
    try {
        const response = await fetch(`${API_URL}/create_link`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ target_url: targetUrl, description }),
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('targetUrl').value = '';
            document.getElementById('description').value = '';
            loadLinks();
        }
    } catch (error) {
        console.error('Erro ao criar link:', error);
    }
}

async function loadLinks() {
    try {
        const response = await fetch(`${API_URL}/links`);
        const links = await response.json();
        
        const linksListElement = document.getElementById('linksList');
        linksListElement.innerHTML = '';
        
        Object.entries(links).forEach(([id, link]) => {
            const linkElement = document.createElement('div');
            linkElement.className = 'link-item';
            linkElement.innerHTML = `
                <h3>${link.description || 'Sem descrição'}</h3>
                <p>Link curto: <a href="/l/${id}" target="_blank">${window.location.origin}/l/${id}</a></p>
                <p>Visitas: ${link.visits}</p>
                <button onclick="viewStats('${id}')">Ver estatísticas</button>
            `;
            linksListElement.appendChild(linkElement);
        });
    } catch (error) {
        console.error('Erro ao carregar links:', error);
    }
}

async function viewStats(linkId) {
    try {
        const response = await fetch(`${API_URL}/stats/${linkId}`);
        const stats = await response.json();
        // Implementar visualização de estatísticas
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

document.getElementById('linkForm').addEventListener('submit', createLink);
window.addEventListener('load', loadLinks); 