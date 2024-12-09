from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.core.jwt.security import get_db, get_current_user
from app.services.item_service import get_all_items, create_item, get_item_by_id

router = APIRouter()

@router.post("/wardrobe/add-item")
def create_user_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_item(db, item, current_user.id)

@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_by_id(db, item_id)

