from pydantic import BaseModel


class WardrobeResponse(BaseModel):
    wardrobe_id: int
    name: str

    class Config:
        from_attributes = True
