from typing import List

from sqlalchemy.orm import Session

from app import models, schemas
from app.core.exceptions import raise_not_found, raise_item_exception
from app.services.wardrobe_service import ADMIN_EMAIL


def validate_category(db: Session, category_id: int):
    category = db.query(models.AllCategories).filter(models.AllCategories.category_id == category_id).first()
    if not category:
        raise_not_found("Invalid category ID.")
    return category


def validate_photos(photos: List[schemas.PhotoCreate]):
    thumbnail_count = sum(1 for photo in photos if photo.is_thumbnail)
    if thumbnail_count > 1:
        raise_item_exception("Only one photo can be marked as a thumbnail.")
    if thumbnail_count == 0:
        raise_item_exception("At least one photo must be marked as a thumbnail.")

def is_url_unique(db: Session, url: str) -> bool:
    return not db.query(models.Photo).filter(models.Photo.url == url).first()


def validate_item_fields(db: Session, item: schemas.ItemCreate | schemas.ItemUpdate, user_email):
    if item.price is not None and item.price <= 0:
        raise_item_exception("Item price must be greater than 0.")
    if item.name is not None and not item.name.strip():
        raise_item_exception("Item name is required.")
    if item.category_id is not None:
        validate_category(db, item.category_id)
    if user_email != ADMIN_EMAIL and item.is_for_rent is not None:
        raise_item_exception("Item can't be on rent for non Admins.")

