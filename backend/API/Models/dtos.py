from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# Customer DTOs
class CustomerBase(BaseModel):
    name: str
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    post_code: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Item DTOs
class ItemBase(BaseModel):
    item_code: str
    description: str
    price: Decimal


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Order Line Item DTOs
class OrderLineItemBase(BaseModel):
    item_id: int
    note: Optional[str] = None
    quantity: int
    price: Decimal
    tax_rate: Decimal


class OrderLineItemCreate(OrderLineItemBase):
    pass


class OrderLineItemResponse(OrderLineItemBase):
    id: int
    sales_order_id: int
    excl_amount: Decimal
    tax_amount: Decimal
    incl_amount: Decimal
    item: Optional[ItemResponse] = None

    model_config = ConfigDict(from_attributes=True)


# Sales Order DTOs
class SalesOrderBase(BaseModel):
    invoice_no: str
    invoice_date: datetime
    reference_no: Optional[str] = None
    note: Optional[str] = None
    customer_id: int


class SalesOrderCreate(SalesOrderBase):
    line_items: List[OrderLineItemCreate]


class SalesOrderUpdate(BaseModel):
    invoice_date: Optional[datetime] = None
    reference_no: Optional[str] = None
    note: Optional[str] = None
    customer_id: Optional[int] = None
    line_items: Optional[List[OrderLineItemCreate]] = None


class SalesOrderResponse(SalesOrderBase):
    id: int
    total_excl: Decimal
    total_tax: Decimal
    total_incl: Decimal
    created_at: datetime
    updated_at: datetime
    customer: Optional[CustomerResponse] = None
    line_items: List[OrderLineItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Sales Order List DTO (for home screen)
class SalesOrderListItem(BaseModel):
    id: int
    invoice_no: str
    invoice_date: datetime
    customer_name: str
    reference_no: Optional[str] = None
    total_excl: Decimal
    total_tax: Decimal
    total_incl: Decimal

    model_config = ConfigDict(from_attributes=True)
