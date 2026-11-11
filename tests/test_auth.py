import pytest
import time
from httpx import AsyncClient, ASGITransport
from app.main import app # qué app ES ESTA?
from app.core import totp

@pytest.mark.asyncio
async def test_full_mfa_flow():
    # Unique email for testing to avoid conflicts
    test_email = f"test_{int(time.time())}@example.com"
    test_password = "mypassword"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        
        # --- STEP 1: Register ---
        res = await client.post("/api/v1/auth/register", json={
            "email": test_email,
            "password": test_password
        })
        assert res.status_code == 200
        data = res.json()
        assert "totp_secret" in data
        secret = data["totp_secret"]

        # --- STEP 2: Login (First Factor) ---
        res = await client.post("/api/v1/auth/login", json={
            "email": test_email,
            "password": test_password
        })
        assert res.status_code == 200
        temp_token = res.json()["temp_token"]

        # --- STEP 3: MFA verification (Second Factor) ---
        # Generate code valid TOTP using the secret
        code = totp._generate_totp(secret)
        
        res = await client.post("/api/v1/auth/verify-mfa", json={
            "temp_token": temp_token,
            "totp_code": code
        })
        assert res.status_code == 200
        tokens = res.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        access_token = tokens["access_token"]

        # --- STEP 4: Access protected route ---
        res = await client.get("/api/v1/users/me", headers={
            "Authorization": f"Bearer {access_token}"
        })
        assert res.status_code == 200
        user_data = res.json()
        assert user_data["email"] == test_email