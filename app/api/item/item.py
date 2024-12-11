from typing import Optional, List

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.core.jwt.security import get_db, get_current_user
from app.services.item_service import create_item, get_item_by_id, get_filtered_items, delete_item, update_item, get_all

router = APIRouter()


@router.get("/items/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_by_id(db, item_id)


@router.get("/items", response_model=List[schemas.ItemResponse])
async def get_filtered_items_route(
    db: Session = Depends(get_db),
    wardrobe_name: Optional[str] = Query(None, description="Filter by wardrobe name"),
    category_name: Optional[str] = Query(None, description="Filter by category name"),
    category_gender: Optional[str] = Query(None, description="Filter by category gender"),
    is_for_rent: Optional[bool] = Query(None, description="Filter by rental status"),
    ascending: Optional[bool] = Query(None, description="Sort by ascending (true) or descending (false) price"),
    search_term: Optional[str] = Query(None, description="Search by item name"),
):
    return get_filtered_items(
        db=db,
        wardrobe_name=wardrobe_name,
        category_name=category_name,
        category_gender=category_gender,
        is_for_rent=is_for_rent,
        ascending=ascending,
        search_term=search_term,
    )

@router.get("/user/wardrobe/items")
def get_items_needing_attention(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_all(db, current_user.id)

@router.post("/user/wardrobe/items/add-item")
async def create_user_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_item(db, item, current_user.id)

@router.delete("/user/wardrobe/items/remove-item")
async def delete_user_item(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_item(db, item_id, current_user.id)

@router.put("/user/wardrobe/items/update-item")
async def update_user_item(update_data: schemas.ItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_item(db, current_user.id, update_data)

