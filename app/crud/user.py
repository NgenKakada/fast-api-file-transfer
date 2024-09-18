from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..schemas import UserCreate
from sqlalchemy.future import select

# Get user by username (Async)
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))  # Async select
    return result.scalars().first()

# Get user by email (Async)
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))  # Async select
    return result.scalars().first()

# Create a new user (Async)
async def create_user(db: AsyncSession, user: UserCreate):
    from ..core import get_password_hash
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    
    db.add(db_user)
    await db.commit()  # Async commit
    await db.refresh(db_user)  # Async refresh
    return db_user
