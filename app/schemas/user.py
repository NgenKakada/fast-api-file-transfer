from pydantic import BaseModel, EmailStr, Field

# Pydantic schema for user creation
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")  # EmailStr adds email validation
    password: str = Field(..., min_length=8, example="strong_password123")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "strong_password123"
            }
        }


# Pydantic schema for returning user information (without password)
class UserOutPut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True  # Enables returning data from the database using ORM
        schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john.doe@example.com",
                "is_active": True
            }
        }
