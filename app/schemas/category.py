from pydantic import BaseModel

from typing import List


class Category(BaseModel):
    category_id: int
    name: str

    class Config:
        orm_mode = True


class CategoryResponse(Category):
    parents: List["CategoryResponse"] | None = []
    children: List["CategoryResponse"] | None = []

    class Config:
        orm_mode = True
