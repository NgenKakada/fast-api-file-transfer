from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base, product_category_association

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    # Many-to-many relationship with Category
    categories = relationship(
        "Category", secondary=product_category_association, back_populates="products"
    )