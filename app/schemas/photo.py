from pydantic import BaseModel


class PhotoResponse(BaseModel):
    photo_id: int
    url: str
    is_thumbnail: bool

    class Config:
        orm_mode = True
