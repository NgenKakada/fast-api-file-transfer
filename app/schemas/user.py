from pydantic import BaseModel

# Pydantic schema for user creation
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Pydantic schema for returning user information (without password)
class UserOutPut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True  # Enables returning data from the database using ORM
