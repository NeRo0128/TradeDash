from pydantic import BaseModel, confloat
from typing import Optional, Dict
from datetime import datetime

class CashReportBase(BaseModel):
    opening_amount: confloat(gt=0)

class CashReportCreate(CashReportBase):
    pass

class CashReportUpdate(BaseModel):
    closing_amount: confloat(gt=0)
    notes: Optional[str] = None

class CashReportResponse(BaseModel):
    id: int
    user_id: int
    opening_amount: float
    closing_amount: Optional[float] = None
    total_sales: float
    total_orders: int
    discrepancy: Optional[float] = None
    notes: Optional[str] = None
    sales_summary: Dict[str, float]
    opened_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True