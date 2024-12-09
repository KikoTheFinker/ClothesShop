from typing import List

from pydantic import BaseModel

from .category import CategoryResponse
from .photo import PhotoCreate, PhotoResponse


class ItemBase(BaseModel):
    name: str
    price: int
    is_price_fixed: bool
    is_for_rent: bool


class ItemResponse(ItemBase):
    item_id: int
    category: CategoryResponse
    photos: List[PhotoResponse]

    class Config:
        from_attributes  = True


class ItemCreate(BaseModel):
    name: str
    price: int
    is_price_fixed: bool
    is_for_rent: bool
    category_id: int
    photos: List[PhotoCreate]


class ItemUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    is_price_fixed: bool | None = None
    is_for_rent: bool | None = None
    category_id: int | None = None
    photos: List[PhotoCreate]
