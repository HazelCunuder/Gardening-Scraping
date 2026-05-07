from sqlalchemy import Column, Integer, String, Float, Text, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    category_name   = Column(String(255))
    url             = Column(String(2048))
    category_id     = Column(String(255))
    parent_category = Column(String(255))
    image_url       = Column(String(2048))


class Product(Base):
    __tablename__ = "product"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    url              = Column(String(2048))
    name             = Column(String(255), nullable=False)
    price_euros      = Column(Float)
    price_cents      = Column(Float)
    price_concat     = Column(Float)
    product_id       = Column(Integer)
    product_code     = Column(Integer)
    product_category = Column(String(255))
    description      = Column(Text)
