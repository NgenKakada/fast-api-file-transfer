from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_user_by_username
from app.db.session import get_db

user_router = APIRouter()

@user_router.post("/create-user")
async def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    new_user = create_user(db, user_data)
    return {"message": "User created successfully", "user": new_user.username}
