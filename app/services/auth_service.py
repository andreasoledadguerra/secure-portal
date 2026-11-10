from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core import totp
from app.core.config import settings
from app.core.listeners import notify_auth_event

async def register_user(db: AsyncSession, email: str, password: str) -> User:
    """Registra un usuario nuevo y genera su secreto TOTP."""
    # Verificar si el email ya existe
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise ValueError("Email already registered")

    # Generar secreto TOTP y crear usuario
    secret = totp.generate_secret()
    user = User(
        email=email,
        hashed_password=hash_password(password),
        totp_secret=secret,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Emitir evento de auditoría
    await notify_auth_event("user_registered", email, {"user_id": user.id})
    return user

async def authenticate_password(db: AsyncSession, email: str, password: str) -> User | None:
    """Verifica email + contraseña (primer factor)."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        await notify_auth_event("password_failed", email, {"reason": "user_not_found"})
        return None

    if not verify_password(password, user.hashed_password):
        await notify_auth_event("password_failed", email, {"reason": "wrong_password"})
        return None

    await notify_auth_event("password_ok", email, {"user_id": user.id})
    return user

async def verify_mfa(db: AsyncSession, user: User, code: str) -> bool:
    """Verifica el código TOTP (segundo factor) con bloqueo por intentos fallidos."""
    now = datetime.now(timezone.utc)

    # Si la cuenta está bloqueada temporalmente, rechazar
    if user.locked_until and user.locked_until > now:
        await notify_auth_event(
            "mfa_locked",
            user.email,
            {"locked_until": user.locked_until.isoformat()},
        )
        return False

    # Verificar el código TOTP
    if totp.verify_totp(user.totp_secret, code):
        user.failed_mfa_attempts = 0
        user.locked_until = None
        await db.commit()
        await notify_auth_event("mfa_ok", user.email, {"user_id": user.id})
        return True

    # Código incorrecto: incrementar contador y aplicar bloqueo si corresponde
    user.failed_login_attempts += 1
    locked = False
    if user.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
        user.locked_until = now + timedelta(minutes=settings.LOCKOUT_MINUTES)
        user.failed_login_attempts = 0
        locked = True
    await db.commit()

    await notify_auth_event(
        "mfa_failed",
        user.email,
        {"attempts": user.failed_login_attempts, "locked": locked},
    )
    return False