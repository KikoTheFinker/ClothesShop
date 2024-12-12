from typing import List

from pydantic import BaseModel

from app.schemas import ItemResponse


class WardrobeBase(BaseModel):
    wardrobe_name: str


class WardrobeCreate(WardrobeBase):
    pass


class WardrobeUpdate(WardrobeBase):
    wardrobe_name: str


class WardrobeResponse(WardrobeBase):
    wardrobe_name: str

    class Config:
        from_attributes = True


class WardrobeItemsResponse(WardrobeResponse):
    user_id: int
    items: List[ItemResponse]

    class Config:
        from_attributes = True
