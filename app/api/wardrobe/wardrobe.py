from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.jwt.security import get_db, get_current_user
from app.schemas import WardrobeResponse
from app.schemas.wardrobe import WardrobeCreate
from app.services.wardrobe_service import create_wardrobe, get_all_wardrobes

router = APIRouter()

@router.post("/create")
def create_user_wardrobe(wardrobe: WardrobeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_wardrobe(db, wardrobe, current_user.id)


@router.get("/", response_model=List[WardrobeResponse])
def get_all_user_wardrobe(db: Session = Depends(get_db)):
    return get_all_wardrobes(db)

