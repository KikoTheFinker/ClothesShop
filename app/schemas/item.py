from pydantic import BaseModel
from typing import List
from .category import CategoryResponse
from .wardrobe import WardrobeResponse
from .photo import PhotoResponse


class Item(BaseModel):
    item_id: int
    name: str
    price: int
    is_price_fixed: bool
    is_for_rent: bool


class ItemResponse(Item):
    category: CategoryResponse
    wardrobe: WardrobeResponse
    photos: List[PhotoResponse] = []

    class Config:
        orm_mode = True
