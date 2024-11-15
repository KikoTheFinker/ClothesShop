from sqlalchemy import String, Integer, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Photo(Base):
    __tablename__ = "photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    is_thumbnail = Column(Boolean, nullable=True)

    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False)

    item = relationship("Item", back_populates="photos")
