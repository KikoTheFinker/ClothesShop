from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter()


@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user_service.create_user(db, user)
    return new_user
