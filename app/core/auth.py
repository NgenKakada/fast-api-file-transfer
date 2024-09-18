from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt  # Using PyJWT instead of authlib.jose for better compatibility
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..crud import get_user_by_username
from .config import settings

# JWT Secret and Algorithm
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for Bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verifying user password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Create JWT token (can be used for both Access and Refresh tokens)
def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Generate the JWT token using PyJWT
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Create Access Token
def create_access_token(data: dict):
    return create_token(data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

# Create Refresh Token
def create_refresh_token(data: dict):
    return create_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

# Decode JWT token
def decode_token(token: str):
    try:
        # Decode the JWT token and validate it using PyJWT
        claims = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return claims
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Asynchronously get the current user from the token, handling the token for the decorator
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    claims = decode_token(token)  # Decode the token
    username = claims.get("sub")  # Get the username (or subject)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # Fetch user from the database asynchronously
    user = await get_user_by_username(db, username=username)  # Ensure get_user_by_username is async
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return {"username": user.username}
