from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services import user_service
from ..schemas.user import UserUpdate, UserResponse
from ..utils.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(user_data: UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await user_service.update_user(db, current_user.id, user_data)

@router.get("/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, current_user = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return await user_service.get_users(db, skip=skip, limit=limit)