from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, index=True, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    is_price_fixed = Column(Boolean, nullable=False)
    is_for_rent = Column(Boolean, nullable=False)

    category_id = Column(Integer, ForeignKey("all_categories.category_id"), nullable=False)
    wardrobe_id = Column(Integer, ForeignKey("wardrobes.wardrobe_id"), nullable=False)

    category = relationship("AllCategories", back_populates="items")
    wardrobe = relationship("Wardrobe", back_populates="items")
    photos = relationship("Photo", back_populates="item")
