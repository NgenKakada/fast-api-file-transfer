import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import product, sftp
from app.core.scheduler import lifespan
from app.core.config import settings 

# Initialize FastAPI app, disabling default docs and redoc generation
app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

# Include routers for 'Home' and 'Products' sections
app.include_router(sftp.router, prefix="/sftp", tags=["Home"])
app.include_router(product.router, prefix="/products", tags=["Products"])

# Basic Authentication setup
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

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/images/favicon.ico")

# Protect Swagger UI with Basic Auth
@app.get("/docs", tags=["documentation"], include_in_schema=False)
def protected_docs(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json", 
        title="API Documentation", 
        swagger_favicon_url="/favicon.ico"
    )

# Protect ReDoc with Basic Auth
@app.get("/redoc", tags=["documentation"], include_in_schema=False)
def protected_redoc(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_redoc_html(
        openapi_url="/openapi.json", 
        title="API ReDoc Documentation", 
        redoc_favicon_url="/favicon.ico"
    )

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="File Transfer & CRUD Operation",
        version="1.0.0",
        description="API for secure SFTP file transfers and CRUD operations for managing products.",
        routes=app.routes,
    )
    openapi_schema["tags"] = [
        {"name": "Home", "description": "Operations related to home services like SFTP transfer."},
        {"name": "Products", "description": "Operations for managing products (CRUD)."}
    ]
    app.openapi_schema = openapi_schema
    return openapi_schema

# Apply custom OpenAPI schema
app.openapi = custom_openapi

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APPLICATION_URL, port=settings.APPLICATION_PORT, reload=True)
