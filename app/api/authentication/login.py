from fastapi import APIRouter, Depends
from app.schemas import UserLogin, UserResponse
from app.services import user_service
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/login', response_model=UserResponse)
async def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(
        db,
        login_data.email,
        login_data.phone_number,
        login_data.password
    )
    return UserResponse.from_orm(user)
