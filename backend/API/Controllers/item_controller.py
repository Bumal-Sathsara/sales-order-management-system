from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Infrastructure.Data.database import get_db
from Application.Services.services import ItemService
from API.Models.dtos import ItemCreate, ItemResponse

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("/", response_model=List[ItemResponse])
def get_all(db: Session = Depends(get_db)):
    service = ItemService(db)
    return service.get_all_items()


@router.get("/{item_id}", response_model=ItemResponse)
def get_by_id(item_id: int, db: Session = Depends(get_db)):
    service = ItemService(db)
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=201)
def create(item: ItemCreate, db: Session = Depends(get_db)):
    service = ItemService(db)
    return service.create_item(item)
