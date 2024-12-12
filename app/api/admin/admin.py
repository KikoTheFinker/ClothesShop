from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.jwt.security import get_db, get_current_user
from app.schemas.category import CreateCategory
from app.services.admin_service import approve_pending_item, add_new_category, get_pending_items, \
    apply_modify_to_pending_item, delete_item_as_admin, delete_wardrobe_as_admin

router = APIRouter()


@router.post("/category/add")
async def add_category(category: CreateCategory, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return add_new_category(category, db, current_user.id)


@router.post("/items/request-modification")
async def request_modification(item_id: int, comment: str, db: Session = Depends(get_db),
                               current_user=Depends(get_current_user)):
    return apply_modify_to_pending_item(db, current_user.email, item_id, comment)


@router.put("/items/approve-item")
async def approve_user_item(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return approve_pending_item(db, current_user.email, item_id)


@router.get("/items/pending")
async def get_pending(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_pending_items(db, current_user.email)


@router.delete("/items/delete/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return delete_item_as_admin(db, item_id, current_user.email)


@router.delete("/wardrobe/delete/{wardrobe_name}")
async def delete_item(wardrobe_name: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_wardrobe_as_admin(db, wardrobe_name, current_user.email)


