from enum import Enum

from pydantic import BaseModel


class GenderEnum(str, Enum):
    MEN = "MAN"
    WOMEN = "WOMAN"
    KID = "KID"
    UNISEX = "UNISEX"
    NO_GENDER = "NO-GENDER"


class Category(BaseModel):
    category_id: int
    name: str

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    name: str
    gender: GenderEnum = GenderEnum.NO_GENDER
    class Config:
        from_attributes = True


CategoryResponse.model_rebuild()
