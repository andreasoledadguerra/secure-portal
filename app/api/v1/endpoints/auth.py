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

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await auth_service.register_user(db, data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return RegisterResponse(
        email=user.email,
        totp_secret=user.totp_secret,
        otpauth_uri=totp.generate_otpauth_uri(user.totp_secret, user.email)
    )

@router.post("/login", response_model=TempTokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate_password(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return TempTokenResponse(temp_token=security.create_temp_token(user.id))