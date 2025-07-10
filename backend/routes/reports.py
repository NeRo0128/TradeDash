from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services import report_service
from ..schemas.report import CashReportCreate, CashReportUpdate, CashReportResponse
from ..utils.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/cash", response_model=CashReportResponse)
async def create_cash_report(report: CashReportCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await report_service.create_cash_report(db, report, current_user)

@router.get("/cash", response_model=List[CashReportResponse])
async def read_cash_reports(skip: int = 0, limit: int = 100, current_user = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return await report_service.get_cash_reports(db, skip=skip, limit=limit)

@router.get("/cash/{report_id}", response_model=CashReportResponse)
async def read_cash_report(report_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await report_service.get_cash_report(db, report_id, current_user)

@router.put("/cash/{report_id}/close", response_model=CashReportResponse)
async def close_cash_report(report_id: int, report: CashReportUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await report_service.close_cash_report(db, report_id, report, current_user)