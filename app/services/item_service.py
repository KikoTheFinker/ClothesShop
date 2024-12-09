from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from .user_service import get_user
from .wardrobe_service import get_wardrobe_by_user_id, ADMIN_EMAIL
from .. import models, schemas
from app.core.exceptions import raise_not_found, raise_item_exception



def validate_category(db: Session, category_id: int):
    category = db.query(models.AllCategories).filter(models.AllCategories.category_id == category_id).first()
    if not category:
        raise_not_found("Invalid category ID.")
    return category

def create_item(db: Session, item: schemas.ItemCreate, user_id: int) -> dict:
    try:

        category = validate_category(db, item.category_id)

        wardrobe = get_wardrobe_by_user_id(db, user_id)

        thumbnail_count = sum(1 for photo in item.photos if photo.is_thumbnail)

        user = get_user(db, user_id)


        if item.price <= 0:
            raise_item_exception("Item price must be greater than 0.")
        if thumbnail_count > 1:
            raise_item_exception("Only one photo can be marked as a thumbnail.")
        if thumbnail_count == 0:
            raise_item_exception("At least one photo must be marked as a thumbnail.")
        if not item.name:
            raise_item_exception("Item name is required.")
        if not item.category_id:
            raise_item_exception("Item category ID is required.")

        if user.email != ADMIN_EMAIL and item.is_for_rent is not None:
            raise_item_exception("Item can't be on rent.")

        db_item = models.Item(
            name=item.name,
            price=item.price,
            is_price_fixed=item.is_price_fixed,
            is_for_rent=item.is_for_rent if user.email == ADMIN_EMAIL else None,
            category_id=category.category_id,
            wardrobe_id=wardrobe.wardrobe_id
        )

        db.add(db_item)
        db.flush()

        photos = [
            models.Photo(
                url=photo.url,
                is_thumbnail=photo.is_thumbnail,
                item_id=db_item.item_id
            )
            for photo in item.photos
        ]
        db.bulk_save_objects(photos)

        db.commit()
        db.refresh(db_item)

        return {"message": "Item created successfully.", "item_id": db_item.item_id}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the item: {str(e)}"
        )


def get_all_items(db: Session) -> List[schemas.ItemResponse]:
    items = db.query(models.Item).all()
    return [schemas.ItemResponse.model_validate(item) for item in items]


def get_item_by_id(db: Session, item_id: int) -> schemas.ItemResponse:
    item = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    if not item:
        raise_not_found("Item not found.")
    return schemas.ItemResponse.model_validate(item)


def get_items_by_wardrobe_id(db: Session, wardrobe_id: int) -> List[schemas.ItemResponse]:
    items = db.query(models.Item).filter(models.Item.wardrobe_id == wardrobe_id).all()
    return [schemas.ItemResponse.model_validate(item) for item in items]


def get_filtered_items(
        db: Session,
        wardrobe_id: int | None = None,
        category_name: str | None = None,
        is_for_rent: bool | None = None,
        ascending: bool | None = None,
        search_term: str | None = None,
) -> List[schemas.ItemResponse]:
    query = db.query(models.Item)

    if wardrobe_id:
        query = query.filter(models.Item.wardrobe_id == wardrobe_id)

    if category_name:
        query = query.join(models.AllCategories).filter(models.AllCategories.name == category_name)

    if is_for_rent is not None:
        query = query.filter(models.Item.is_for_rent == is_for_rent)

    if search_term:
        search_term = search_term.strip()
        query = query.filter(models.Item.name.ilike(f"%{search_term}%"))

    if ascending is not None:
        order = models.Item.price.asc() if ascending else models.Item.price.desc()
        query = query.order_by(order)

    items = query.all()

    if not items:
        raise_not_found("No items found matching the given criteria.")

    return [schemas.ItemResponse.model_validate(item) for item in items]


def delete_item(db: Session, item_id: int) -> dict:
    item = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    if not item:
        raise_not_found("Item not found.")

    db.delete(item)
    db.flush()
    return {"message": "Item deleted successfully."}
