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