from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.jwt.security import get_current_user
from app.db.database import get_db
from app.services.photo_service import update_thumbnail, remove_photo

router = APIRouter()


@router.put("/photo/edit-thumbnail")
async def edit_photo_thumbnail(item_id: int, photo_id: int, db: Session = Depends(get_db),
                               current_user=Depends(get_current_user)):
    return update_thumbnail(db, current_user.id, item_id, photo_id)


@router.delete("/photo/delete-photo")
async def delete_photo(item_id: int, photo_id: int, db: Session = Depends(get_db),
                       current_user=Depends(get_current_user)):
    return remove_photo(db, current_user.id, item_id, photo_id)
