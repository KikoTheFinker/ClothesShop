from typing import List

from sqlalchemy.orm import Session

from ..models.category import AllCategories
from ..schemas.category import CategoryResponse


def get_all_categories(db: Session) -> List[CategoryResponse]:
    categories = db.query(AllCategories).all()
    return [CategoryResponse.model_validate(category) for category in categories]
