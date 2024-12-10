from sqlalchemy.orm import Session

from app import models
from app.core.exceptions import raise_forbidden, raise_not_found, raise_item_exception
from app.services.item_service import get_raw_item_by_id


def update_thumbnail(db: Session, user_id: int, item_id: int, photo_id: int) -> dict:
    item = get_raw_item_by_id(db, item_id)

    if item.wardrobe.user_id != user_id:
        raise_forbidden("You are not authorized to update the thumbnail for this item.")

    photo = (
        db.query(models.Photo)
        .filter(models.Photo.photo_id == photo_id, models.Photo.item_id == item.item_id)
        .first()
    )

    if not photo:
        raise_not_found("Photo not found for the specified item.")

    for item_photo in item.photos:
        item_photo.is_thumbnail = False

    photo.is_thumbnail = True

    db.commit()
    db.refresh(item)

    return {"message": "Thumbnail updated successfully."}


def remove_photo(db: Session, user_id: int, item_id: int, photo_id: int) -> dict:
    item = get_raw_item_by_id(db, item_id)

    if item.wardrobe.user_id != user_id:
        raise_forbidden("You are not authorized to remove photos from this item.")

    photo = (
        db.query(models.Photo)
        .filter(models.Photo.photo_id == photo_id, models.Photo.item_id == item.item_id)
        .first()
    )

    if not photo:
        raise_not_found("Photo not found for the specified item.")

    if photo.is_thumbnail:
        raise_item_exception("Cannot remove a photo marked as a thumbnail. Update the thumbnail first.")

    db.delete(photo)
    db.commit()

    return {"message": "Photo removed successfully."}
