from functools import wraps
from fastapi import Request, HTTPException, status
from app.core.auth import get_current_user

def login_required(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authentication token"
            )

        try:
            # Extract and validate token using get_current_user
            db = kwargs.get("db")  # Ensure `db` is passed to the decorator
            token_data = await get_current_user(token.split(" ")[1], db)  # Assumes "Bearer <token>"
            request.state.user = token_data  # Store the user data in request state
            print(token_data)
        
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        
        return await fn(*args, **kwargs)
    
    return wrapper
