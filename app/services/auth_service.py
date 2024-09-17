from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core import auth
from app.crud import get_user_by_username

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, username: str, password: str):
        user = get_user_by_username(self.db, username)
        if not user or not auth.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def generate_tokens(self, username: str):
        # Use the username directly in both tokens
        access_token = auth.create_access_token(data={"sub": username})
        refresh_token = auth.create_refresh_token(data={"sub": username})
        
        return access_token, refresh_token

    def validate_refresh_token(self, refresh_token: str):
        claims = auth.decode_token(refresh_token)
        username = claims.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
