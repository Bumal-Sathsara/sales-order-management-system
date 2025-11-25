from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Infrastructure.Data.database import get_db
from Application.Services.services import CustomerService
from API.Models.dtos import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("/", response_model=List[CustomerResponse])
def get_all(db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_all_customers()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_by_id(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerResponse, status_code=201)
def create(customer: CustomerCreate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.create_customer(customer)
