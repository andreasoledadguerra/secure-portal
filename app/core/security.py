from datetime import datetime,timedelta, timezone
from jose import jwt,JWTError #type: ignore
from passlib.context import CryptContext #type: ignore
from constants import SECRET_KEY, ALGORITHM
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__truncate_error=False)

#SECRET_KEY = "your-secret-key"  # usar variable de entorno
#ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 15
#REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
#TEMP_TOKEN_EXPIRE_MINUTES = 5  # para el paso MFA

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_jwt(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(user_id: int) -> str:
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_jwt({"sub": str(user_id), "type": "access"}, expire)

def create_refresh_token(user_id: int) -> str:
    expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_jwt({"sub": str(user_id), "type": "refresh"}, expire)

def create_temp_token(user_id: int) -> str:
    expire = timedelta(minutes=settings.TEMP_TOKEN_EXPIRE_MINUTES)
    return create_jwt({"sub": str(user_id), "type": "temp"}, expire)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])