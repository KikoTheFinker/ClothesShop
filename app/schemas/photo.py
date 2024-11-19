from pydantic import BaseModel


class PhotoResponse(BaseModel):
    photo_id: int
    url: str
    is_thumbnail: bool

    class Config:
        from_attributes = True


class PhotoCreate(BaseModel):
    url: str
    is_thumbnail: bool
