from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Infrastructure.Data.database import get_db
from Application.Services.services import SalesOrderService
from API.Models.dtos import (
    SalesOrderCreate, SalesOrderResponse,
    SalesOrderUpdate, SalesOrderListItem
)

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/", response_model=List[SalesOrderListItem])
def get_all(db: Session = Depends(get_db)):
    service = SalesOrderService(db)
    return service.get_all_orders()


@router.get("/{order_id}", response_model=SalesOrderResponse)
def get_by_id(order_id: int, db: Session = Depends(get_db)):
    service = SalesOrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=SalesOrderResponse, status_code=201)
def create(order: SalesOrderCreate, db: Session = Depends(get_db)):
    service = SalesOrderService(db)
    return service.create_order(order)


@router.put("/{order_id}", response_model=SalesOrderResponse)
def update(
    order_id: int,
    order_update: SalesOrderUpdate,
    db: Session = Depends(get_db)
):
    service = SalesOrderService(db)
    order = service.update_order(order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=204)
def delete(order_id: int, db: Session = Depends(get_db)):
    service = SalesOrderService(db)
    if not service.delete_order(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return None
