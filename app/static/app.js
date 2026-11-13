let tempToken = null;

// Función para alternar entre Register y Login
function showSection(sectionId) {
    // Ocultar ambas secciones primero
    document.getElementById('register-section').classList.add('hidden');
    document.getElementById('login-section').classList.add('hidden');
    
    // Mostrar solo la sección seleccionada
    document.getElementById(sectionId).classList.remove('hidden');
    
    // Ocultar el menú de navegación (para no distraer durante el proceso)
    document.getElementById('nav-menu').classList.add('hidden');
    
    // Limpiar mensajes de error anteriores
    document.getElementById('reg-result').innerText = '';
    document.getElementById('login-result').innerText = '';
}

async function register() {
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const res = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
        // Mostrar el panel con el secreto TOTP
        document.getElementById('mfa-setup').classList.remove('hidden');
        document.getElementById('totp-secret').innerText = data.totp_secret;
        document.getElementById('otpauth-uri').innerText = data.otpauth_uri;
        document.getElementById('reg-result').innerText = "Registration successful! You can now Login.";
        document.getElementById('reg-result').className = 'success';
    } else {
        document.getElementById('reg-result').innerText = data.detail;
        document.getElementById('reg-result').className = 'error';
    }
}

async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
        tempToken = data.temp_token;
        // Mostrar el campo para el código de 6 dígitos
        document.getElementById('mfa-verify').classList.remove('hidden');
        document.getElementById('login-result').innerText = "Password verified. Enter your TOTP code.";
        document.getElementById('login-result').className = 'success';
    } else {
        document.getElementById('login-result').innerText = data.detail;
        document.getElementById('login-result').className = 'error';
    }
}

async function verifyMfa() {
    const code = document.getElementById('totp-code').value;
    const res = await fetch('/api/v1/auth/verify-mfa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ temp_token: tempToken, totp_code: code })
    });
    const data = await res.json();
    if (res.ok) {
        document.getElementById('login-result').innerText = "Success! Access Token: " + data.access_token.substring(0, 20) + "...";
        document.getElementById('login-result').className = 'success';
    } else {
        document.getElementById('login-result').innerText = data.detail;
        document.getElementById('login-result').className = 'error';
    }
}