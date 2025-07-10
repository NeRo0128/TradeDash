from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services import order_service
from ..schemas.order import OrderCreate, OrderUpdate, OrderResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await order_service.create_order(db, order, current_user)

@router.get("/", response_model=List[OrderResponse])
async def read_orders(skip: int = 0, limit: int = 100, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await order_service.get_orders(db, current_user, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await order_service.get_order(db, order_id, current_user)

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order: OrderUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await order_service.update_order(db, order_id, order, current_user)

@router.put("/{order_id}/complete", response_model=OrderResponse)
async def complete_order(order_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await order_service.complete_order(db, order_id, current_user)

@router.put("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await order_service.cancel_order(db, order_id, current_user)