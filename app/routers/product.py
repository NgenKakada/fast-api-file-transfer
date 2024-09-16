from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import ProductCreate, ProductResponse, ProductUpdate
from ..crud import (create_product, delete_product, get_product, get_products,
    update_product)

product_router  = APIRouter()

@product_router.post("/", response_model=ProductResponse)
def create_product_route(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data)

@product_router.get("/", response_model=list[ProductResponse])
def get_products_route(db: Session = Depends(get_db)):
    return get_products(db)

@product_router.get("/{product_id}", response_model=ProductResponse)
def get_product_route(product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id)

@product_router.put("/{product_id}", response_model=ProductResponse)
def update_product_route(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
        return update_product(db, product_id, product_data)
    
@product_router.delete("/{product_id}")
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return {"detail": "Product deleted successfully"}