from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.database import get_db
from app.core import security, totp
from app.schemas.auth import (
    RegisterRequest, RegisterResponse, 
    LoginRequest, TempTokenResponse, 
    VerifyMFARequest, TokenResponse, RefreshRequest
)
from app.services import auth_service
from app.models.user import User