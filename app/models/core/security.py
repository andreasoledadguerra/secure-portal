from datetime import datetime,timedelta, timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from constants import SECRET_KEY, ALGORITHM

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

def create_jwt(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])