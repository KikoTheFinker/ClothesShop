from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from .user_service import get_user
from .wardrobe_service import ADMIN_EMAIL
from ..core.exceptions import raise_forbidden
from ..models.category import AllCategories
from ..schemas.category import CreateCategory, CategoryResponse


def add_new_category(category: CreateCategory, db: Session, user_id: int) -> dict:
    user = get_user(db, user_id)
    if user.email != ADMIN_EMAIL:
        raise raise_forbidden("Only admins can add new categories.")

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


def get_all_categories(db: Session) -> List[CategoryResponse]:
    categories = db.query(AllCategories).all()
    return [CategoryResponse.model_validate(category) for category in categories]
