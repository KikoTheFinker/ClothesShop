from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.schemas.category import GenderEnum


class AllCategories(Base):
    __tablename__ = "all_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False, default=GenderEnum.NO_GENDER.value)

    items = relationship("Item", back_populates="category")

