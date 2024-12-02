from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas


ADMIN_EMAIL = "test.test@gmail.com"
def create_wardrobe(db:Session, wardrobe:schemas.WardrobeCreate, user_id: int) -> dict:

    existing_wardrobe = db.query(models.Wardrobe).filter(models.Wardrobe.user_id == user_id).first()
    if existing_wardrobe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A wardrobe for this user already exists."
        )
    db_wardrobe = models.Wardrobe(
        price=wardrobe.price,
        subscription_date=date.today(),
        wardrobe_name=wardrobe.name,
        user_id=user_id,
    )
    db.add(db_wardrobe)
    db.commit()
    db.refresh(db_wardrobe)

    return {"message": "Created wardrobe successfully."}

