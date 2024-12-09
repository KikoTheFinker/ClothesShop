from pydantic import BaseModel


class WardrobeBase(BaseModel):
    wardrobe_name: str


class WardrobeCreate(WardrobeBase):
    pass


class WardrobeUpdate(WardrobeBase):
    wardrobe_name: str


class WardrobeResponse(WardrobeBase):
    wardrobe_id: int

    class Config:
        from_attributes = True

