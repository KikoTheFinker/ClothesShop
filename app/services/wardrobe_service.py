from datetime import date
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Wardrobe
from .. import models, schemas
from ..core.exceptions import raise_wardrobe_conflict


def create_wardrobe(db: Session, wardrobe: schemas.WardrobeCreate, user_id: int) -> dict:
    existing_wardrobe = get_wardrobe_by_user_id(db, user_id)
    if existing_wardrobe:
        raise raise_wardrobe_conflict("A wardrobe for this user already exists.")

    existing_wardrobe_name = db.query(Wardrobe).filter(
        func.lower(Wardrobe.wardrobe_name) == wardrobe.wardrobe_name.lower()).first()
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
    wardrobes = db.query(Wardrobe).all()
    return [schemas.WardrobeResponse.model_validate(wardrobe) for wardrobe in wardrobes]


def get_wardrobe_by_user_id(db: Session, user_id: int) -> models.Wardrobe:
    return db.query(Wardrobe).filter(Wardrobe.user_id == user_id).first()


def delete_wardrobe(db: Session, user_id: int):
    wardrobe = get_wardrobe_by_user_id(db, user_id)
    if not wardrobe:
        raise raise_wardrobe_conflict("A wardrobe does not exist.")

    db.delete(wardrobe)
    db.commit()

    return {"message": "Deleted wardrobe successfully."}


def update_wardrobe(db: Session, wardrobe: schemas.WardrobeUpdate, user_id: int):
    db_wardrobe = get_wardrobe_by_user_id(db, user_id)
    if not db_wardrobe:
        raise raise_wardrobe_conflict("A wardrobe does not exist.")

    if not wardrobe.wardrobe_name:
        raise raise_wardrobe_conflict("A wardrobe update name does not exist.")

    existing_wardrobe = db.query(models.Wardrobe).filter(
        models.Wardrobe.wardrobe_name == wardrobe.wardrobe_name,
        models.Wardrobe.wardrobe_id != db_wardrobe.wardrobe_id
    ).first()

    if existing_wardrobe:
        raise raise_wardrobe_conflict(f"The wardrobe name '{wardrobe.wardrobe_name}' is already in use.")

    db_wardrobe.wardrobe_name = wardrobe.wardrobe_name
    db.commit()
    db.refresh(db_wardrobe)

    return {"message": "Updated wardrobe successfully."}


def get_items_in_wardrobe(db: Session, wardrobe_name: str) -> schemas.WardrobeItemsResponse:
    from ..services.item_service import get_items_by_wardrobe_id

    wardrobe = db.query(models.Wardrobe).filter(models.Wardrobe.wardrobe_name == wardrobe_name).first()
    if not wardrobe:
        raise raise_wardrobe_conflict("A wardrobe with this name does not exist.")

    items = get_items_by_wardrobe_id(db, wardrobe.wardrobe_id)

    wardrobe_response = schemas.WardrobeItemsResponse.model_validate({
        "user_id": wardrobe.user_id,
        "wardrobe_id": wardrobe.wardrobe_id,
        "wardrobe_name": wardrobe.wardrobe_name,
        "items": [schemas.ItemResponse.model_validate(item) for item in items],
    })
    return wardrobe_response
