from pydantic import BaseModel, confloat
from typing import List, Optional
from datetime import datetime

class OrderProductBase(BaseModel):
    product_id: int
    quantity: int
    price_at_time: float

class OrderCreate(BaseModel):
    products: List[OrderProductBase]

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderProductResponse(OrderProductBase):
    id: int
    name: str

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    products: List[OrderProductResponse]

    class Config:
        from_attributes = True