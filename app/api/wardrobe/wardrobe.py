from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.jwt.security import get_db, get_current_user
from app.schemas.wardrobe import WardrobeCreate
from app.services.wardrobe_service import create_wardrobe

router = APIRouter()

router.post("/create")
def create_wardrobe_endpoint(wardrobe: WardrobeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_wardrobe(db, wardrobe, current_user.id)
