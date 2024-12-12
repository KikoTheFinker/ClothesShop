from datetime import date
from typing import List

from pydantic import BaseModel

from .category import CategoryResponse
from .photo import PhotoCreate, PhotoResponse
from ..models.item import ItemStatus


class ItemBase(BaseModel):
    name: str
    price: int
    is_price_fixed: bool
    is_for_rent: bool


class ItemResponse(ItemBase):
    item_id: int
    wardrobe_name: str | None = None
    creation_date: date
    status: ItemStatus
    category: CategoryResponse
    photos: List[PhotoResponse]

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class ItemResponseWithComment(ItemResponse):
    comment: str | None = None


class ItemCreate(BaseModel):
    name: str
    price: int
    is_price_fixed: bool
    is_for_rent: bool | None = None
    category_id: int
    photos: List[PhotoCreate]


class ItemUpdate(BaseModel):
    item_id: int
    name: str | None = None
    price: int | None = None
    is_price_fixed: bool | None = None
    is_for_rent: bool | None = None
    category_id: int | None = None
    status: ItemStatus = ItemStatus.PENDING_REVIEW
    photos: List[PhotoCreate] | None = None

    class Config:
        from_attributes = True
