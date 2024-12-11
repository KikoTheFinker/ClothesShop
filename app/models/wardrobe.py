from sqlalchemy import Integer, Date, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Wardrobe(Base):
    __tablename__ = "wardrobes"

    wardrobe_id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False)
    subscription_date = Column(Date, nullable=False)
    wardrobe_name = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    owner = relationship("User", back_populates="wardrobe", uselist=False)
    items = relationship("Item", back_populates="wardrobe", cascade="all, delete-orphan")
