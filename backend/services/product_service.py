from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate

async def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

async def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

async def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

async def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    db_product = await get_product(db, product_id)
    if not db_product:
        return None

    for field, value in product.dict(exclude_unset=True).items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product

async def delete_product(db: Session, product_id: int) -> None:
    db_product = await get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()