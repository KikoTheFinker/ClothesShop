from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    city = Column(String(50), nullable=True)
    country = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)

    wardrobe = relationship("Wardrobe", back_populates="owner", uselist=False)
