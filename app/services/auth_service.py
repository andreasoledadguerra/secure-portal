from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core import totp
from app.core.config import settings
from app.core.listeners import notify_auth_event