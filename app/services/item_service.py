from typing import List

from fastapi import HTTPException, status
from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import raise_not_found, raise_forbidden, raise_item_exception, raise_wardrobe_conflict
from .user_service import get_user
from .validators.item_validator import validate_item_fields, validate_category, validate_photos, is_url_unique
from .wardrobe_service import get_wardrobe_by_user_id
from .. import models, schemas
from ..core.jwt.config import ADMIN_EMAIL


def create_item(db: Session, item: schemas.ItemCreate, user_id: int) -> dict:
    try:
        if item.category_id is not None:
            category = validate_category(db, item.category_id)

        wardrobe = get_wardrobe_by_user_id(db, user_id)
        if not wardrobe:
            raise_wardrobe_conflict("A wardrobe for this user does not exist.")

        user = get_user(db, user_id)

        validate_item_fields(db, item, user.email)

        if len(item.photos) > 3:
            raise_item_exception("An item can have a maximum of 3 photos.")

        validate_photos(item.photos)



        for photo in item.photos:
            if not is_url_unique(db, photo.url):
                raise_item_exception(f"The URL '{photo.url}' is already in use.")

        item_status = (
            models.ItemStatus.PENDING_REVIEW
            if user.email != ADMIN_EMAIL
            else models.ItemStatus.APPROVED
        )

        db_item = models.Item(
            name=item.name,
            price=item.price,
            is_price_fixed=item.is_price_fixed,
            is_for_rent=item.is_for_rent if user.email == ADMIN_EMAIL else False,
            category_id=category.category_id,
            wardrobe_id=wardrobe.wardrobe_id,
            status = item_status
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

        if item_status == models.ItemStatus.PENDING_REVIEW:
            db_item_review = models.ItemReview(
                item_id=db_item.item_id,
            )
            db.add(db_item_review)

        db.commit()
        db.refresh(db_item)

        return {"message": "Item created successfully.", "item_id": db_item.item_id}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the item: {str(e)}"
        )


def get_item_by_id(db: Session, item_id: int) -> schemas.ItemResponse:
    result = (
        db.query(models.Item, models.Wardrobe.wardrobe_name.label("wardrobe_name"))
        .join(models.Wardrobe, models.Item.wardrobe_id == models.Wardrobe.wardrobe_id)
        .filter(models.Item.item_id == item_id)
        .filter(models.Item.status == models.ItemStatus.APPROVED)
        .first()
    )

    if not result:
        raise_not_found("Item not found.")

    item, wardrobe_name = result

    return schemas.ItemResponse(
        name=item.name,
        price=item.price,
        is_price_fixed=item.is_price_fixed,
        is_for_rent=item.is_for_rent,
        item_id=item.item_id,
        status=item.status,
        wardrobe_name=wardrobe_name,
        creation_date=item.creation_date,
        category=item.category,
        photos=item.photos,
    )


def get_items_by_wardrobe_id(db: Session, wardrobe_id: int) -> List[schemas.ItemResponse]:
    items = db.query(models.Item).filter(models.Item.wardrobe_id == wardrobe_id).filter(models.Item.status == models.ItemStatus.APPROVED).all()
    return [schemas.ItemResponse.model_validate(item) for item in items]


def get_filtered_items(
        db: Session,
        wardrobe_name: str | None = None,
        category_name: str | None = None,
        category_gender: str | None = None,
        is_for_rent: bool | None = None,
        ascending: bool | None = None,
        search_term: str | None = None,
) -> List[schemas.ItemResponse]:

    query = (
        db.query(models.Item, models.Wardrobe.wardrobe_name.label("wardrobe_name"))
        .join(models.Wardrobe, models.Item.wardrobe_id == models.Wardrobe.wardrobe_id)
        .join(models.AllCategories, models.Item.category_id == models.AllCategories.category_id)
        .filter(models.Item.status == models.ItemStatus.APPROVED)
    )

    if wardrobe_name:
        query = query.filter(models.Wardrobe.wardrobe_name == wardrobe_name)

    if category_name:
        query = query.filter(models.AllCategories.name.ilike(category_name))

    if category_gender:
        query = query.filter(models.AllCategories.gender.cast(String).ilike(category_gender))

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

    return [
        schemas.ItemResponse(
            **item.Item.__dict__,
            wardrobe_name=item.wardrobe_name,
            category=item.Item.category,
            photos=item.Item.photos
        )
        for item in items
    ]


def get_raw_item_by_id(db: Session, item_id: int) -> models.Item:
    item = (
        db.query(models.Item)
        .join(models.Wardrobe, models.Item.wardrobe_id == models.Wardrobe.wardrobe_id)
        .filter(models.Item.item_id == item_id)
        .first()
    )

    if not item:
        raise_not_found("Item not found.")

    return item


def delete_item(db: Session, item_id: int, user_id: int) -> dict:
    item = get_raw_item_by_id(db, item_id)

    if item.wardrobe.user_id != user_id:
        raise_forbidden("You are not authorized to delete this item.")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted successfully."}

def get_all(db: Session, user_id: int) -> List[schemas.ItemResponse]:
    items = (
        db.query(models.Item)
        .join(models.Wardrobe, models.Item.wardrobe_id == models.Wardrobe.wardrobe_id)
        .filter(models.Wardrobe.user_id == user_id)
        .all()
    )
    return [schemas.ItemResponse.model_validate(item) for item in items]



def update_item(db: Session, user_id: int, update_data: schemas.ItemUpdate) -> dict:
    item = get_raw_item_by_id(db, update_data.item_id)

    if item.wardrobe.user_id != user_id:
        raise_forbidden("You are not authorized to edit this item.")

    if update_data.category_id is not None:
        validate_category(db, update_data.category_id)

    user = get_user(db, user_id)

    validate_item_fields(db, update_data, user.email)

    item.status = models.ItemStatus.PENDING_REVIEW


    for key, value in update_data.model_dump(exclude_unset=True).items():
        if key not in ["item_id", "photos", "status"]:
            setattr(item, key, value)

    if update_data.photos:
        existing_photo_count = db.query(models.Photo).filter(models.Photo.item_id == item.item_id).count()
        if len(item.photos) + existing_photo_count > 3:
             raise_item_exception("An item can have a maximum of 3 photos.")
        for photo in update_data.photos:
            if photo.is_thumbnail:
                raise_item_exception(
                    "Cannot mark a new photo as a thumbnail here. Use update_thumbnail instead.")

            if not is_url_unique(db, photo.url):
                raise_item_exception(f"The URL '{photo.url}' is already in use.")

            existing_photo = (
                db.query(models.Photo)
                .filter(models.Photo.url == photo.url, models.Photo.item_id == item.item_id)
                .first()
            )
            if not existing_photo:
                new_photo = models.Photo(
                    url=photo.url,
                    is_thumbnail=False,
                    item_id=item.item_id
                )
                db.add(new_photo)

    db.commit()
    db.refresh(item)

    return {"message": "Item updated successfully."}

