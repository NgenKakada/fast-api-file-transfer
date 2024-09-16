from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

# Association table for many-to-many relationship between Product and Category
product_category_association = Table(
    'product_category_association', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)