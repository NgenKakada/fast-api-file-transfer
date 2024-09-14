from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.models.product import Product

# CREATE
def create_product(db:Session, product_data: ProductCreate)-> ProductResponse:
    try:
        product = Product(**product_data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        
        return ProductResponse.from_orm(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# READ (Single Product)
def read_product(db: Session, product_id: int) -> ProductResponse:
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        print("Query executed, product found:", product)  # Debugging output

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductResponse.from_orm(product)

    except Exception as e:
        print("Error during querying the product:", str(e))  # Debugging output
        raise HTTPException(status_code=500, detail=str(e))
    
# READ ALL (List of Products)
def read_products(db:Session)-> list[ProductResponse]:
    products = db.query(Product).all()
    return [ProductResponse.from_orm(product) for product in products]

# UPDATE
def update_product(db:Session, product_id: int, update_data: ProductUpdate)-> ProductResponse:
    product = read_product(db, product_id)
    if product:
        for var, value in update_data.dict(exclude_unset=True).items():
            setattr(product, var, value)
        db.commit()
        return ProductResponse.from_orm(product)
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# DELETE
def delete_product(db: Session, product_id: int):
    # Retrieve the actual product from the database
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
