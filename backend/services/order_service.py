from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException

from ..models.order import Order, order_products
from ..models.product import Product
from ..models.user import User
from ..schemas.order import OrderCreate, OrderUpdate

async def create_order(db: Session, order: OrderCreate, user: User) -> Order:
    # Calcular el monto total y verificar stock
    total_amount = 0
    products_data = []
    
    for item in order.products:
        product = await get_product(db, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        total_amount += product.price * item.quantity
        products_data.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "price_at_time": product.price
        })
        
        # Actualizar stock
        product.stock -= item.quantity
    
    # Crear orden
    db_order = Order(
        user_id=user.id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(db_order)
    db.flush()
    
    # Agregar productos a la orden
    for product_data in products_data:
        stmt = order_products.insert().values(
            order_id=db_order.id,
            **product_data
        )
        db.execute(stmt)
    
    db.commit()
    db.refresh(db_order)
    return db_order

async def get_order(db: Session, order_id: int, user: User) -> Optional[Order]:
    query = db.query(Order).filter(Order.id == order_id)
    if not user.is_admin:
        query = query.filter(Order.user_id == user.id)
    return query.first()

async def get_orders(db: Session, user: User, skip: int = 0, limit: int = 100) -> List[Order]:
    query = db.query(Order)
    if not user.is_admin:
        query = query.filter(Order.user_id == user.id)
    return query.offset(skip).limit(limit).all()

async def update_order(db: Session, order_id: int, order: OrderUpdate, user: User) -> Optional[Order]:
    db_order = await get_order(db, order_id, user)
    if not db_order:
        return None

    for field, value in order.dict(exclude_unset=True).items():
        setattr(db_order, field, value)

    db.commit()
    db.refresh(db_order)
    return db_order

async def complete_order(db: Session, order_id: int, user: User) -> Optional[Order]:
    db_order = await get_order(db, order_id, user)
    if not db_order:
        return None

    db_order.status = "completed"
    db_order.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(db_order)
    return db_order

async def cancel_order(db: Session, order_id: int, user: User) -> Optional[Order]:
    db_order = await get_order(db, order_id, user)
    if not db_order or db_order.status != "pending":
        return None

    # Restaurar stock
    for item in db_order.products:
        product = await get_product(db, item.product_id)
        if product:
            product.stock += item.quantity

    db_order.status = "cancelled"
    db.commit()
    db.refresh(db_order)
    return db_order