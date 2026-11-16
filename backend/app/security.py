from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from .config import settings
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(value): return pwd.hash(value)
def verify_password(value, hashed): return pwd.verify(value, hashed)
def make_token(uid):
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode({"sub":str(uid),"exp":exp}, settings.jwt_secret, algorithm="HS256")
