from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, JSON
from sqlalchemy.sql import func
from . import Base

class CashReport(Base):
    __tablename__ = "cash_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    opening_amount = Column(Float)
    closing_amount = Column(Float)
    total_sales = Column(Float)
    total_orders = Column(Integer)
    discrepancy = Column(Float)  # Diferencia entre lo esperado y lo real
    notes = Column(String, nullable=True)
    sales_summary = Column(JSON)  # Resumen de ventas por producto
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)