from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import ProductCreate, ProductResponse, ProductUpdate
from ..crud import (create_product, delete_product, get_product, get_products, update_product)
from app.decorators.auth_decorator import login_required

product_router = APIRouter()

@product_router.post("/", response_model=ProductResponse)
@login_required
async def create_product_route(request: Request, product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data)

@product_router.get("/", response_model=list[ProductResponse])
@login_required
async def get_products_route(request: Request, db: Session = Depends(get_db)):
    return get_products(db)

@product_router.get("/{product_id}", response_model=ProductResponse)
@login_required
async def get_product_route(request: Request, product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id)

@product_router.put("/{product_id}", response_model=ProductResponse)
@login_required
async def update_product_route(request: Request, product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db, product_id, product_data)

@product_router.delete("/{product_id}")
@login_required
async def delete_product_route(request: Request, product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return {"detail": "Product deleted successfully"}
