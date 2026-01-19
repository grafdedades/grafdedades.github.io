const CONFIG = {
    // Remplaza con tu Client ID de GitHub
    clientId: 'Ov23liRho4N8PKiNCoo1', 
    // URL del Google Apps Script desplegado
    scriptUrl: 'https://script.google.com/macros/s/AKfycbw7oHVXu1vyuDNzmQ66JJV5zON-9RMCu0j-Zmvwiimst4Y8mBlThI5GcNr2TcrkYPjF/exec',
    // URL de redirección (debe coincidir con la configurada en GitHub)
    redirectUri: window.location.origin + '/callback.html'
};

const Auth = {
    login: (isAdmin = false) => {
        // Scopes: 'read:user,user:email' para usuarios, 'repo,read:user,user:email' para admins
        // Nota: Si es admin, pedimos 'repo' para poder crear PRs
        const scope = isAdmin ? 'repo,read:user,user:email' : 'read:user,user:email';
        
        const authUrl = `https://github.com/login/oauth/authorize?client_id=${CONFIG.clientId}&scope=${scope}&redirect_uri=${CONFIG.redirectUri}`;
        
        // Guardar estado para saber a dónde volver tras el login (por defecto root o graph)
        const returnUrl = window.location.pathname.includes('admin') ? 'admin.html' : 'graph.html';
        localStorage.setItem('auth_return_url', returnUrl);
        
        window.location.href = authUrl;
    },

    handleCallback: async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const error = urlParams.get('error');
        const code = urlParams.get('code');

        if (error) {
            console.error("OAuth Error:", error);
            alert("Accés denegat: L'usuari ha cancel·lat l'autorització.");
            window.location.href = 'graph.html';
            return;
        }

        if (!code) return;

        try {
            // Mostrar estado de carga si hay UI
            if (document.getElementById('status')) {
                document.getElementById('status').innerText = 'Autenticando con GitHub...';
            }

            const response = await fetch(`${CONFIG.scriptUrl}?action=auth&code=${code}`);
            const data = await response.json();

            if (data.access_token) {
                // Guardar token
                localStorage.setItem('gh_token', data.access_token);
                
                // Fetch info del usuario para guardar rol/login (opcional pero útil)
                await Auth.fetchUserInfo(data.access_token);

                // Redirigir
                const returnUrl = localStorage.getItem('auth_return_url') || 'graph.html';
                localStorage.removeItem('auth_return_url');
                window.location.href = returnUrl;
            } else {
                console.error('Error Auth:', data);
                alert('Error de autenticación: ' + JSON.stringify(data));
                window.location.href = 'index.html';
            }
        } catch (error) {
            console.error('Error de red:', error);
            alert('Error de conexión con el servidor de autenticación');
        }
    },

    fetchUserInfo: async (token) => {
        try {
            const resp = await fetch('https://api.github.com/user', {
                headers: { 'Authorization': `token ${token}` }
            });
            const user = await resp.json();
            localStorage.setItem('gh_user', JSON.stringify(user));
            return user;
        } catch (e) {
            console.error('Error fetching user:', e);
        }
    },

    logout: () => {
        localStorage.removeItem('gh_token');
        localStorage.removeItem('gh_user');
        window.location.href = 'index.html';
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('gh_token');
    },

    getUser: () => {
        const u = localStorage.getItem('gh_user');
        return u ? JSON.parse(u) : null;
    },
    
    getToken: () => {
         return localStorage.getItem('gh_token');
    }
};
