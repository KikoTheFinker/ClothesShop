from datetime import date
from typing import List
from ..core.exceptions import raise_wardrobe_conflict
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from app.models import Wardrobe


ADMIN_EMAIL = "test.test@gmail.com"
def create_wardrobe(db:Session, wardrobe:schemas.WardrobeCreate, user_id: int) -> dict:
    existing_wardrobe = db.query(Wardrobe).filter(Wardrobe.user_id == user_id).first()
    if existing_wardrobe:
       raise raise_wardrobe_conflict("A wardrobe for this user already exists.")

    existing_wardrobe_name = db.query(Wardrobe).filter(Wardrobe.wardrobe_name == wardrobe.wardrobe_name).first()
    if existing_wardrobe_name:
        raise_wardrobe_conflict(f"A wardrobe with the name '{wardrobe.wardrobe_name}' already exists.")

    db_wardrobe = Wardrobe(
        price=200,
        subscription_date=date.today(),
        wardrobe_name=wardrobe.wardrobe_name,
        user_id=user_id,
    )
    db.add(db_wardrobe)
    db.commit()
    db.refresh(db_wardrobe)

    return {"message": "Created wardrobe successfully."}

def get_all_wardrobes(db: Session) -> List[schemas.WardrobeResponse]:
    wardrobes =  db.query(Wardrobe).all()
    return [schemas.WardrobeResponse.model_validate(wardrobe) for wardrobe in wardrobes]