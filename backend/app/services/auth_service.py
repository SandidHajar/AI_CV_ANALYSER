from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config.settings import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def get_password_hash(self, password: str) -> str:
        # bcrypt has a 72-byte limit. We truncate to 72 chars to be safe.
        return pwd_context.hash(password[:72])

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password[:72], hashed_password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            return payload
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Token decode error: {e}")
            print(f"Token decode error: {e}")
            return None

auth_service = AuthService()
