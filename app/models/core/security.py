from datetime import datetime,timedelta, timezone
from jose import jwt,JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#SECRET_KEY = "your-secret-key"  # usar variable de entorno
#ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 15
#REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
#TEMP_TOKEN_EXPIRE_MINUTES = 5  # para el paso MFA

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
