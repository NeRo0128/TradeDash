from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.user import User
from ..schemas.user import UserUpdate
from . import auth_service

async def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

async def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

async def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

async def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
        
    for field, value in user_data.dict(exclude_unset=True).items():
        if field == "password" and value:
            value = auth_service.get_password_hash(value)
            field = "hashed_password"
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user