from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.jwt.security import get_current_user
from app.db.database import get_db
from app.schemas.category import CreateCategory
from app.services.category_service import add_new_category, get_all_categories

router = APIRouter()


@router.post("/category/add", response_model=dict)
async def add_category(category: CreateCategory, db: Session = Depends(get_db),  current_user=Depends(get_current_user)):
    return add_new_category(category, db, current_user.id)


@router.get("/category/all")
async def get_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)