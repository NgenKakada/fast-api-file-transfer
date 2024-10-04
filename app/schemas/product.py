from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, strip_whitespace=True, example="Example Product Name")
    description: str = Field(..., min_length=10, max_length=1000, strip_whitespace=True, example="Detailed description of the product.")
    price: float = Field(..., gt=0, le=100000, example=19.99)

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "name": "Example Product Name",
                "description": "This is a sample product description with at least 10 characters.",
                "price": 19.99
            }
        }


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str = Field(None, min_length=1, max_length=100, strip_whitespace=True, example="Updated Product Name")
    description: str = Field(None, min_length=10, max_length=1000, strip_whitespace=True, example="Updated product description.")
    price: float = Field(None, gt=0, le=100000, example=24.99)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Example Product Name",
                "description": "This is a sample product description with at least 10 characters.",
                "price": 19.99
            }
        }
