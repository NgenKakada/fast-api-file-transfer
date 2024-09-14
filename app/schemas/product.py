from pydantic import BaseModel, Field, validator, constr

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, strip_whitespace=True, example="Example Product Name")
    description: str = Field(..., min_length=10, max_length=1000, strip_whitespace=True, example="Detailed description of the product.")
    price: float = Field(..., gt=0, le=100000, example=19.99)

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True
