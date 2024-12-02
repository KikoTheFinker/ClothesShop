from pydantic import BaseModel


class WardrobeBase(BaseModel):
    name: str


class WardrobeCreate(WardrobeBase):
    pass


class WardrobeUpdate(WardrobeBase):
    name: str | None = None


class WardrobeResponse(WardrobeBase):
    wardrobe_id: int

    class Config:
        orm_mode = True
