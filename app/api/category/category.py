from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.category_service import get_all_categories

router = APIRouter()

@router.get("/category/all")
async def get_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)