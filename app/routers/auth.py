from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.auth_service import AuthService

auth_router = APIRouter()

@auth_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token, refresh_token = auth_service.generate_tokens(user.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@auth_router.post("/refresh")
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    # Validate the refresh token and get the username
    username = auth_service.validate_refresh_token(refresh_token)
    # Pass the username to generate new access token
    new_access_token, _ = auth_service.generate_tokens(username)
    
    return {"access_token": new_access_token, "token_type": "bearer"}
