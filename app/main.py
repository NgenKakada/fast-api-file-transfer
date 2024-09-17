from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi
from app.routers import sftp_router, product_router, auth_router, user_router
from app.core import lifespan, settings
from app.utils.security import protected_docs, protected_redoc

# Initialize FastAPI app, disabling default docs and redoc generation
app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

# Include routers
app.include_router(sftp_router, prefix="/sftp", tags=["Home"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(user_router, tags=["User"])

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/images/favicon.ico")

# Protect Swagger UI and ReDoc with Basic Auth
app.get("/docs", include_in_schema=False)(protected_docs)
app.get("/redoc", include_in_schema=False)(protected_redoc)

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
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APPLICATION_URL, port=settings.APPLICATION_PORT, reload=True)
