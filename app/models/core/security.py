from datetime import datetime,timedelta, timezone
from jose import jwt,JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
