from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from .. import models, schemas
from app.core.exceptions import raise_not_found


def create_item(db: Session, item: schemas.ItemCreate) -> dict:
    try:
        with ((db.begin())):
            db_category = db.query(models.AllCategories
                                   ).filter(models.AllCategories.category_id == item.category_id).first()
            if not db_category:
                raise_not_found("Invalid category ID.")

            db_wardrobe = db.query(models.Wardrobe).filter(models.Wardrobe.wardrobe_id == item.wardrobe_id).first()
            if not db_wardrobe:
                raise_not_found("Invalid wardrobe ID.")

            db_item = models.Item(
                name=item.name,
                price=item.price,
                is_price_fixed=item.is_price_fixed,
                is_for_rent=item.is_for_rent,
                category_id=db_category.category_id,
                wardrobe_id=db_wardrobe.wardrobe_id
            )
            db.add(db_item)
            db.flush()

            db_photos = [
                models.Photo(
                    url=photo.url,
                    is_thumbnail=photo.is_thumbnail,
                    item_id=db_item.item_id
                )
                for photo in item.photos
            ]
            db.bulk_save_objects(db_photos)

        return {"message": "Item created successfully.", "item_id": db_item.item_id}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the item."
        )
