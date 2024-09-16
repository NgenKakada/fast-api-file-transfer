from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base, product_category_association

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Many-to-many relationship with Product
    products = relationship(
        "Product", secondary=product_category_association, back_populates="categories"
    )