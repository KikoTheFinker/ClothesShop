from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services import user_service
from app.schemas.user import UserCreate, UserResponse
from app.db.database import get_db

router = APIRouter()


@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)
    new_user = user_service.create_user(db, user)
    return new_user
