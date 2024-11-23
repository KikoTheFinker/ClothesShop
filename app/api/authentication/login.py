from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.jwt.security import create_access_token
from app.db.database import get_db
from app.schemas import UserLogin
from app.services import user_service

router = APIRouter()


@router.post('/login', response_model=None)
async def login_user(response: Response, login_data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(
        db,
        login_data.email,
        login_data.phone_number,
        login_data.password
    )
    access_token = create_access_token(data={"sub": user.email})

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax',
        expires=3600
    )

    return {"message": "Login successful"}
