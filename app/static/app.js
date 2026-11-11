let tempToken = null;

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
        document.getElementById('register-section').classList.add('hidden');
        document.getElementById('mfa-setup').classList.remove('hidden');
        document.getElementById('totp-secret').innerText = data.totp_secret;
        document.getElementById('otpauth-uri').innerText = data.otpauth_uri;
    } else {
        document.getElementById('reg-result').innerText = data.detail;
        document.getElementById('reg-result').className = 'error';
    }
}

function showLogin() {
    document.getElementById('mfa-setup').classList.add('hidden');
    document.getElementById('login-title').classList.remove('hidden');
    document.getElementById('login-section').classList.remove('hidden');
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
        document.getElementById('mfa-verify').classList.remove('hidden');
        document.getElementById('login-result').innerText = "Ingresa tu código TOTP";
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
        document.getElementById('login-result').innerText = "¡Éxito! Access Token: " + data.access_token.substring(0, 20) + "...";
        document.getElementById('login-result').className = 'success';
    } else {
        document.getElementById('login-result').innerText = data.detail;
        document.getElementById('login-result').className = 'error';
    }
}