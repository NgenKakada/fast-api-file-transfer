from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from sqlalchemy.orm import Session
from app.crud.product import (create_product, delete_product, get_product, get_products,
    update_product)

router  = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product_route(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data)

@router.get("/", response_model=list[ProductResponse])
def get_products_route(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_route(product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_route(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
        return update_product(db, product_id, product_data)
    
@router.delete("/{product_id}")
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return {"detail": "Product deleted successfully"}