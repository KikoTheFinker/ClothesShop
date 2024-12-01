from fastapi import APIRouter, Depends

from app.core.jwt.security import get_current_user
from app.schemas import UserResponse

router = APIRouter()

@router.get("/status", response_model=dict)
async def check_status(current_user: UserResponse = Depends(get_current_user)):
    return {"email": current_user.email}
