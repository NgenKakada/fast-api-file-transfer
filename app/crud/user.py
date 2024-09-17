# app/crud/user.py
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate

# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Create a new user
def create_user(db: Session, user: UserCreate):
    from ..core import get_password_hash
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
