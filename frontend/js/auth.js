const API_BASE = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    // Determine the current page
    const path = window.location.pathname;
    const isAuthPage = path === '/login' || path.endsWith('login.html') || path === '/register' || path.endsWith('register.html');
    
    // Check authentication immediately
    const token = localStorage.getItem('siem_jwt_token');
    
    // Auth Guard
    if (!token && !isAuthPage) {
        // Redirection block: unauthorized user trying to view secure pages
        window.location.href = '/login';
        return;
    }
    
    if (token && isAuthPage) {
        // Logged-in user trying to view login page: send to dashboard
        window.location.href = '/';
        return;
    }

    // Attach form handlers
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Attach logout to any button with id 'logout-btn'
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById('login-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Authenticating...';
    btn.disabled = true;

    try {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success && data.token) {
            localStorage.setItem('siem_jwt_token', data.token);
            localStorage.setItem('siem_username', data.user.username);
            
            // Redirect to dashboard
            window.location.href = '/';
        } else {
            showError(data.message || 'Invalid credentials');
        }
    } catch (err) {
        showError('Could not connect to the authentication server.');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById('register-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
    btn.disabled = true;

    try {
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (data.success) {
            // Auto login after registration
            await handleLoginFlow(username, password);
        } else {
            showError(data.message || 'Registration failed');
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    } catch (err) {
        showError('Could not connect to the authentication server.');
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Inner login wrapper used by register
async function handleLoginFlow(username, password) {
    const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    if (data.success) {
        localStorage.setItem('siem_jwt_token', data.token);
        localStorage.setItem('siem_username', data.user.username);
        window.location.href = '/';
    } else {
        window.location.href = '/login';
    }
}

function logout(e) {
    if (e) e.preventDefault();
    localStorage.removeItem('siem_jwt_token');
    localStorage.removeItem('siem_username');
    window.location.href = '/login';
}

// Global utility for API injection
window.getAuthHeaders = function() {
    const token = localStorage.getItem('siem_jwt_token');
    if (!token) {
        logout();
        return { 'Content-Type': 'application/json' };
    }
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
};

// Global interceptor to nuke broken/expired tokens preventing death-loops
const originalFetch = window.fetch;
window.fetch = async function() {
    try {
        const response = await originalFetch.apply(this, arguments);
        // If the backend refuses our token, obliterate it and throw us back to login instantly
        if (response.status === 401) {
            console.warn("401 Unauthorized - Destroying token intercept");
            logout();
        }
        return response;
    } catch(err) {
        throw err;
    }
};
