import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.core import settings

# HTTP Basic Auth setup
security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not (secrets.compare_digest(credentials.username, settings.DOC_USERNAME) and
            secrets.compare_digest(credentials.password, settings.DOC_PASSWORD)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Protect Swagger UI with Basic Auth
def protected_docs(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json", 
        title="API Documentation", 
        swagger_favicon_url="/favicon.ico"
    )

# Protect ReDoc with Basic Auth
def protected_redoc(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_redoc_html(
        openapi_url="/openapi.json", 
        title="API ReDoc Documentation", 
        redoc_favicon_url="/favicon.ico"
    )
