import os
from datetime import datetime, timedelta, timezone

import redis
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/app_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

try:
    cache = redis.Redis.from_url(settings.redis_url, decode_responses=True)
except Exception:
    cache = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
app = FastAPI(title="fastapi-production-starter")
auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": username, "exp": expire}, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
    except JWTError:
        username = None
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return username


class TokenRequest(BaseModel):
    username: str


@auth_router.post("/token")
def login(body: TokenRequest):
    # Stub: replace with a real user lookup and password check.
    return {"access_token": create_access_token(body.username), "token_type": "bearer"}


app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/me")
def me(username: str = Depends(get_current_user)):
    return {"username": username}


@app.get("/cached/{key}")
def cached(key: str):
    if cache is not None:
        try:
            value = cache.get(key)
            if value is not None:
                return {"key": key, "value": value, "cached": True}
            cache.setex(key, 60, f"value-for-{key}")
        except Exception:
            pass
    return {"key": key, "value": f"value-for-{key}", "cached": False}
