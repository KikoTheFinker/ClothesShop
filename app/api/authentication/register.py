from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import UserCreate, MessageResponse
from app.services import user_service

router = APIRouter()


@router.post('/register', response_model=MessageResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    message = user_service.create_user(db, user)
    return message
