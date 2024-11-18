from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from .. import models, schemas
from app.core.exceptions import raise_not_found


def validate_category(db: Session, category_id: int):
    category = db.query(models.AllCategories).filter(models.AllCategories.category_id == category_id).first()
    if not category:
        raise_not_found("Invalid category ID.")
    return category


def validate_wardrobe(db: Session, wardrobe_id: int):
    wardrobe = db.query(models.Wardrobe).filter(models.Wardrobe.wardrobe_id == wardrobe_id).first()
    if not wardrobe:
        raise_not_found("Invalid wardrobe ID.")
    return wardrobe


def create_item(db: Session, item: schemas.ItemCreate) -> dict:
    try:
        with db.begin():
            category = validate_category(db, item.category_id)
            wardrobe = validate_wardrobe(db, item.wardrobe_id)

            db_item = models.Item(
                name=item.name,
                price=item.price,
                is_price_fixed=item.is_price_fixed,
                is_for_rent=item.is_for_rent,
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

        return {"message": "Item created successfully.", "item_id": db_item.item_id}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the item: {str(e)}"
        )


def get_all_items(db: Session) -> List[schemas.ItemResponse]:
    items = db.query(models.Item).all()
    return [schemas.ItemResponse.from_orm(item) for item in items]


def get_item_by_id(db: Session, item_id: int) -> schemas.ItemResponse:
    item = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    if not item:
        raise_not_found("Item not found.")
    return schemas.ItemResponse.from_orm(item)


def get_items_by_wardrobe_id(db: Session, wardrobe_id: int) -> List[schemas.ItemResponse]:
    items = db.query(models.Item).filter(models.Item.wardrobe_id == wardrobe_id).all()
    return [schemas.ItemResponse.from_orm(item) for item in items]


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

    return [schemas.ItemResponse.from_orm(item) for item in items]


def delete_item(db: Session, item_id: int) -> dict:
    item = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    if not item:
        raise_not_found("Item not found.")

    db.delete(item)
    db.flush()
    return {"message": "Item deleted successfully."}
