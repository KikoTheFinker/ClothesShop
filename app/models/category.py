from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class CategoryRelations(Base):
    __tablename__ = "category_relations"

    parent_category_id = Column(Integer, ForeignKey("all_categories.category_id"), primary_key=True)
    child_category_id = Column(Integer, ForeignKey("all_categories.category_id"), primary_key=True)


class AllCategories(Base):
    __tablename__ = "all_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    items = relationship("Item", back_populates="category")

    parents = relationship(
        "AllCategories",
        secondary="category_relations",
        primaryjoin=category_id == CategoryRelations.child_category_id,
        secondaryjoin=category_id == CategoryRelations.parent_category_id,
        backref="children"
    )
