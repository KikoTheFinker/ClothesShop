from sqlalchemy import Column, Integer, String
from app.db.database import Base


class ItemReview(Base):
    __tablename__ = 'item_reviews'

    review_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, index=True)
    comment = Column(String, nullable=False, default='Your item is waiting for review.')

