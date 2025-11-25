from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from Domain.Entities.models import Customer, Item, SalesOrder, OrderLineItem
from Application.Interfaces.repository_interfaces import (
    ICustomerRepository, IItemRepository, ISalesOrderRepository
)


class CustomerRepository(ICustomerRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Customer]:
        return self.db.query(Customer).all()

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def create(self, customer_data: dict) -> Customer:
        db_customer = Customer(**customer_data)
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer


class ItemRepository(IItemRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Item]:
        return self.db.query(Item).all()

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return self.db.query(Item).filter(Item.id == item_id).first()

    def create(self, item_data: dict) -> Item:
        db_item = Item(**item_data)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item


class SalesOrderRepository(ISalesOrderRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[SalesOrder]:
        return self.db.query(SalesOrder).all()

    def get_by_id(self, order_id: int) -> Optional[SalesOrder]:
        return self.db.query(SalesOrder).filter(SalesOrder.id == order_id).first()

    def create(self, order_data: dict) -> SalesOrder:
        line_items_data = order_data.pop('line_items', [])
        db_order = SalesOrder(**order_data)
        
        total_excl = Decimal(0)
        total_tax = Decimal(0)
        total_incl = Decimal(0)
        
        for line_data in line_items_data:
            quantity = Decimal(line_data['quantity'])
            price = Decimal(line_data['price'])
            tax_rate = Decimal(line_data['tax_rate'])
            
            excl_amount = quantity * price
            tax_amount = excl_amount * (tax_rate / Decimal(100))
            incl_amount = excl_amount + tax_amount
            
            line_item = OrderLineItem(
                item_id=line_data['item_id'],
                note=line_data.get('note', ''),
                quantity=line_data['quantity'],
                price=line_data['price'],
                tax_rate=line_data['tax_rate'],
                excl_amount=excl_amount,
                tax_amount=tax_amount,
                incl_amount=incl_amount
            )
            db_order.line_items.append(line_item)
            
            total_excl += excl_amount
            total_tax += tax_amount
            total_incl += incl_amount
        
        db_order.total_excl = total_excl
        db_order.total_tax = total_tax
        db_order.total_incl = total_incl
        
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def update(self, order_id: int, order_data: dict) -> Optional[SalesOrder]:
        db_order = self.get_by_id(order_id)
        if not db_order:
            return None
        
        line_items_data = order_data.pop('line_items', None)
        
        for key, value in order_data.items():
            if hasattr(db_order, key):
                setattr(db_order, key, value)
        
        if line_items_data is not None:
            for line_item in db_order.line_items:
                self.db.delete(line_item)
            
            total_excl = Decimal(0)
            total_tax = Decimal(0)
            total_incl = Decimal(0)
            
            for line_data in line_items_data:
                quantity = Decimal(line_data['quantity'])
                price = Decimal(line_data['price'])
                tax_rate = Decimal(line_data['tax_rate'])
                
                excl_amount = quantity * price
                tax_amount = excl_amount * (tax_rate / Decimal(100))
                incl_amount = excl_amount + tax_amount
                
                line_item = OrderLineItem(
                    item_id=line_data['item_id'],
                    note=line_data.get('note', ''),
                    quantity=line_data['quantity'],
                    price=line_data['price'],
                    tax_rate=line_data['tax_rate'],
                    excl_amount=excl_amount,
                    tax_amount=tax_amount,
                    incl_amount=incl_amount
                )
                db_order.line_items.append(line_item)
                
                total_excl += excl_amount
                total_tax += tax_amount
                total_incl += incl_amount
            
            db_order.total_excl = total_excl
            db_order.total_tax = total_tax
            db_order.total_incl = total_incl
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def delete(self, order_id: int) -> bool:
        db_order = self.get_by_id(order_id)
        if not db_order:
            return False
        
        self.db.delete(db_order)
        self.db.commit()
        return True
