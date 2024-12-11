from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.jwt.security import get_db, get_current_user
from app.schemas import WardrobeResponse
from app.schemas.wardrobe import WardrobeCreate, WardrobeUpdate
from app.services.wardrobe_service import create_wardrobe, get_all_wardrobes, delete_wardrobe, update_wardrobe, \
    get_items_in_wardrobe

router = APIRouter()

@router.post("/create")
async def create_user_wardrobe(wardrobe: WardrobeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_wardrobe(db, wardrobe, current_user.id)

@router.get("/all", response_model=List[WardrobeResponse])
async def get_all_user_wardrobe(db: Session = Depends(get_db)):
    return get_all_wardrobes(db)

@router.get("/{wardrobe_name}")
async def get_all_items_in_wardrobe(wardrobe_name: str, db: Session = Depends(get_db)):
    return get_items_in_wardrobe(db, wardrobe_name)

@router.delete("/delete")
async def delete_user_wardrobe(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_wardrobe(db, current_user.id)

@router.put("/update")
async def update_user_wardrobe(wardrobe: WardrobeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_wardrobe(db, wardrobe, current_user.id)
