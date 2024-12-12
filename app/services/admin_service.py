from typing import List

from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.exceptions import raise_forbidden, raise_item_exception
from app.core.jwt.config import ADMIN_EMAIL
from app.schemas.category import CreateCategory
from app.services.item_service import get_raw_item_by_id
from .user_service import get_user
from ..models import AllCategories


def check_admin(user_email: str):
    if user_email != ADMIN_EMAIL:
        raise raise_forbidden("Only admin")


def add_new_category(category: CreateCategory, db: Session, user_id: int) -> dict:
    user = get_user(db, user_id)
    check_admin(user.email)

    existing_category = (
        db.query(AllCategories)
        .filter(
            func.lower(AllCategories.name) == func.lower(category.name), AllCategories.gender == category.gender)
        .first()
    )

    if existing_category:
        raise raise_forbidden(f"Category '{category.name}' with gender '{category.gender}' already exists.")

    db_category = AllCategories(
        name=category.name,
        gender=category.gender,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {"Message": f"Category '{db_category.name}' with gender '{db_category.gender}' was successfully added."}


def get_pending_items(db: Session, user_email: str) -> List[schemas.ItemResponse]:
    check_admin(user_email)

    items = (
        db.query(models.Item, models.Wardrobe.wardrobe_name.label("wardrobe_name"))
        .join(models.Wardrobe, models.Item.wardrobe_id == models.Wardrobe.wardrobe_id)
        .filter(models.Item.status == models.ItemStatus.PENDING_REVIEW)
        .all()
    )

    return [
        schemas.ItemResponse(
            **item.Item.__dict__,
            wardrobe_name=item.wardrobe_name,
            category=item.Item.category,
            photos=item.Item.photos
        )
        for item in items
    ]


def delete_item_as_admin(db: Session, item_id: int, user_email: str) -> dict:
    check_admin(user_email)
    item = get_raw_item_by_id(db, item_id)

    if not item:
        raise raise_item_exception(f"Item '{item_id}' does not exist.")

    db.delete(item)
    db.commit()

    return {"Message": "item was successfully deleted."}


def delete_wardrobe_as_admin(db: Session, wardrobe_name: str, user_email: str) -> dict:
    check_admin(user_email)
    wardrobe = db.query(models.Wardrobe).filter(models.Wardrobe.wardrobe_name == wardrobe_name).first()

    if not wardrobe:
        raise raise_item_exception(f"Wardrobe '{wardrobe_name}' does not exist.")

    db.delete(wardrobe)
    db.commit()

    return {"Message": "item was successfully deleted."}


def approve_pending_item(db: Session, user_email: str, item_id: int) -> dict:
    check_admin(user_email)

    item = get_raw_item_by_id(db, item_id)

    if item.status != models.ItemStatus.PENDING_REVIEW:
        raise_item_exception("Only items with PENDING_REVIEW status can be approved.")

    item.status = models.ItemStatus.APPROVED
    item.creation_date = func.now()
    db.commit()
    db.refresh(item)

    return {"message": f"Item {item_id} approved successfully."}


def apply_modify_to_pending_item(db: Session, user_email: str, item_id: int, comment: str) -> dict:
    check_admin(user_email)

    item = get_raw_item_by_id(db, item_id)
    if item.status != models.ItemStatus.PENDING_REVIEW:
        raise_item_exception("Only items with PENDING_REVIEW status can be changed to MODIFICATION_REQUIRED.")

    item.status = models.ItemStatus.MODIFICATION_REQUIRED
    review_item = db.query(models.ItemReview).filter(models.ItemReview.item_id == item.item_id).first()
    if review_item:
        review_item.comment = comment
    else:
        review_item = models.ItemReview(item_id=item.item_id, comment=comment)
        db.add(review_item)

    db.commit()
    db.refresh(review_item)

    return {
        "message": f"Item {item_id} marked as MODIFICATION_REQUIRED.",
        "review_comment": comment,
    }