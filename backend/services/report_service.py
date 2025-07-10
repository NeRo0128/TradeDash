from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime
from fastapi import HTTPException

from ..models.report import CashReport
from ..models.order import Order
from ..models.user import User
from ..schemas.report import CashReportCreate, CashReportUpdate

async def create_cash_report(db: Session, report: CashReportCreate, user: User) -> CashReport:
    # Verificar si hay un reporte abierto
    open_report = db.query(CashReport).filter(
        CashReport.user_id == user.id,
        CashReport.closed_at == None
    ).first()
    
    if open_report:
        raise HTTPException(status_code=400, detail="There is already an open cash report")
    
    db_report = CashReport(
        user_id=user.id,
        opening_amount=report.opening_amount,
        total_sales=0,
        total_orders=0,
        sales_summary={}
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

async def get_cash_report(db: Session, report_id: int, user: User) -> Optional[CashReport]:
    query = db.query(CashReport).filter(CashReport.id == report_id)
    if not user.is_admin:
        query = query.filter(CashReport.user_id == user.id)
    return query.first()

async def get_cash_reports(db: Session, skip: int = 0, limit: int = 100) -> List[CashReport]:
    return db.query(CashReport).offset(skip).limit(limit).all()

async def close_cash_report(db: Session, report_id: int, report_data: CashReportUpdate, user: User) -> Optional[CashReport]:
    db_report = await get_cash_report(db, report_id, user)
    if not db_report or db_report.closed_at:
        return None

    # Calcular ventas totales y resumen
    start_time = db_report.opened_at
    end_time = datetime.utcnow()
    
    orders = db.query(Order).filter(
        Order.user_id == user.id,
        Order.status == "completed",
        Order.created_at >= start_time,
        Order.created_at <= end_time
    ).all()

    total_sales = 0
    sales_summary: Dict[str, float] = {}

    for order in orders:
        total_sales += order.total_amount
        for product in order.products:
            product_name = product.name
            if product_name in sales_summary:
                sales_summary[product_name] += product.price_at_time * product.quantity
            else:
                sales_summary[product_name] = product.price_at_time * product.quantity

    # Actualizar reporte
    db_report.closing_amount = report_data.closing_amount
    db_report.total_sales = total_sales
    db_report.total_orders = len(orders)
    db_report.sales_summary = sales_summary
    db_report.discrepancy = db_report.closing_amount - (db_report.opening_amount + total_sales)
    db_report.notes = report_data.notes
    db_report.closed_at = end_time

    db.commit()
    db.refresh(db_report)
    return db_report