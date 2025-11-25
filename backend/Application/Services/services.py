from sqlalchemy.orm import Session
from typing import List, Optional
from Infrastructure.Repositories.repositories import (
    CustomerRepository, ItemRepository, SalesOrderRepository
)
from API.Models.dtos import (
    CustomerCreate, CustomerResponse,
    ItemCreate, ItemResponse,
    SalesOrderCreate, SalesOrderResponse, SalesOrderUpdate, SalesOrderListItem
)


class CustomerService:
    
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def get_all_customers(self) -> List[CustomerResponse]:
        customers = self.repository.get_all()
        return [CustomerResponse.model_validate(c) for c in customers]

    def get_customer(self, customer_id: int) -> Optional[CustomerResponse]:
        customer = self.repository.get_by_id(customer_id)
        return CustomerResponse.model_validate(customer) if customer else None

    def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        customer_data = customer.model_dump()
        db_customer = self.repository.create(customer_data)
        return CustomerResponse.model_validate(db_customer)


class ItemService:
    
    def __init__(self, db: Session):
        self.repository = ItemRepository(db)

    def get_all_items(self) -> List[ItemResponse]:
        items = self.repository.get_all()
        return [ItemResponse.model_validate(i) for i in items]

    def get_item(self, item_id: int) -> Optional[ItemResponse]:
        item = self.repository.get_by_id(item_id)
        return ItemResponse.model_validate(item) if item else None

    def create_item(self, item: ItemCreate) -> ItemResponse:
        item_data = item.model_dump()
        db_item = self.repository.create(item_data)
        return ItemResponse.model_validate(db_item)


class SalesOrderService:
    
    def __init__(self, db: Session):
        self.repository = SalesOrderRepository(db)

    def get_all_orders(self) -> List[SalesOrderListItem]:
        orders = self.repository.get_all()
        result = []
        for order in orders:
            result.append(SalesOrderListItem(
                id=order.id,
                invoice_no=order.invoice_no,
                invoice_date=order.invoice_date,
                customer_name=order.customer.name if order.customer else "",
                reference_no=order.reference_no,
                total_excl=order.total_excl,
                total_tax=order.total_tax,
                total_incl=order.total_incl
            ))
        return result

    def get_order(self, order_id: int) -> Optional[SalesOrderResponse]:
        order = self.repository.get_by_id(order_id)
        return SalesOrderResponse.model_validate(order) if order else None

    def create_order(self, order: SalesOrderCreate) -> SalesOrderResponse:
        order_data = order.model_dump()
        db_order = self.repository.create(order_data)
        return SalesOrderResponse.model_validate(db_order)

    def update_order(self, order_id: int, order_update: SalesOrderUpdate) -> Optional[SalesOrderResponse]:
        order_data = order_update.model_dump(exclude_unset=True)
        db_order = self.repository.update(order_id, order_data)
        return SalesOrderResponse.model_validate(db_order) if db_order else None

    def delete_order(self, order_id: int) -> bool:
        return self.repository.delete(order_id)
