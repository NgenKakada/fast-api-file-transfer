from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..schemas import ProductCreate, ProductResponse, ProductUpdate
from ..crud import create_product, delete_product, get_product, get_products, update_product
from app.decorators.auth_decorator import login_required

product_router = APIRouter()

# Async create product route
@product_router.post("/", response_model=ProductResponse)
@login_required
async def create_product_route(request: Request, product_data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, product_data)

# Async get all products route
@product_router.get("/", response_model=list[ProductResponse])
@login_required
async def get_products_route(request: Request, db: AsyncSession = Depends(get_db)):
    return await get_products(db)

# Async get single product route
@product_router.get("/{product_id}", response_model=ProductResponse)
@login_required
async def get_product_route(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    return await get_product(db, product_id)

# Async update product route
@product_router.put("/{product_id}", response_model=ProductResponse)
@login_required
async def update_product_route(request: Request, product_id: int, product_data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await update_product(db, product_id, product_data)

# Async delete product route
@product_router.delete("/{product_id}")
@login_required
async def delete_product_route(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    await delete_product(db, product_id)
    return {"detail": "Product deleted successfully"}
