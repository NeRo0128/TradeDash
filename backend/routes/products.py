from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services import product_service
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..utils.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, current_user = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return await product_service.create_product(db, product)

@router.get("/", response_model=List[ProductResponse])
async def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return await product_service.get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    return await product_service.get_product(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, current_user = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return await product_service.update_product(db, product_id, product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, current_user = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    await product_service.delete_product(db, product_id)