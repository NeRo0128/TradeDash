from pydantic import BaseModel, conint, confloat
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: confloat(gt=0)

class ProductCreate(ProductBase):
    stock: conint(ge=0) = 0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[confloat(gt=0)] = None
    stock: Optional[conint(ge=0)] = None

class ProductResponse(ProductBase):
    id: int
    stock: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True