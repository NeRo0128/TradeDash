from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from . import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    stock = Column(Integer, default=0)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())