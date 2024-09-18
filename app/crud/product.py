from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.models import Product
from sqlalchemy.future import select

# CREATE (Async)
async def create_product(db: AsyncSession, product_data: ProductCreate) -> ProductResponse:
    try:
        product = Product(**product_data.model_dump())
        db.add(product)
        await db.commit()  # Async commit
        await db.refresh(product)  # Async refresh
        
        return ProductResponse.from_orm(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET (Single Product, Async)
async def get_product(db: AsyncSession, product_id: int) -> ProductResponse:
    try:
        result = await db.execute(select(Product).filter(Product.id == product_id))  # Async select
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductResponse.from_orm(product)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET ALL (List of Products, Async)
async def get_products(db: AsyncSession) -> list[ProductResponse]:
    try:
        result = await db.execute(select(Product))  # Async select
        products = result.scalars().all()  # Get all products
        return [ProductResponse.from_orm(product) for product in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# UPDATE (Async)
async def update_product(db: AsyncSession, product_id: int, update_data: ProductUpdate) -> ProductResponse:
    product = await get_product(db, product_id)  # Fetch the product using async get function
    if product:
        for var, value in update_data.dict(exclude_unset=True).items():
            setattr(product, var, value)
        await db.commit()  # Async commit
        await db.refresh(product)  # Async refresh
        return ProductResponse.from_orm(product)
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# DELETE (Async)
async def delete_product(db: AsyncSession, product_id: int):
    try:
        result = await db.execute(select(Product).filter(Product.id == product_id))  # Async select
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        await db.delete(product)  # Async delete
        await db.commit()  # Async commit
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
