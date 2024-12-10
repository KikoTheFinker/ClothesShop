from enum import Enum

from pydantic import BaseModel


class GenderEnum(str, Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"
    KID = "KID"
    UNISEX = "UNISEX"
    NO_GENDER = "NO_GENDER"


class Category(BaseModel):
    category_id: int
    name: str

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    category_id: int
    name: str
    gender: GenderEnum = GenderEnum.NO_GENDER

    class Config:
        from_attributes = True


class CreateCategory(BaseModel):
    name: str
    gender: GenderEnum = GenderEnum.NO_GENDER

    class Config:
        from_attributes = True

