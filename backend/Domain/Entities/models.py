from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from Infrastructure.Data.database import Base


class Customer(Base):
    """Customer entity with address information"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    address1 = Column(String(255))
    address2 = Column(String(255))
    address3 = Column(String(255))
    suburb = Column(String(100))
    state = Column(String(100))
    post_code = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sales_orders = relationship("SalesOrder", back_populates="customer")


class Item(Base):
    """Item/Product entity"""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order_line_items = relationship("OrderLineItem", back_populates="item")


class SalesOrder(Base):
    """Sales Order header entity"""
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String(50), unique=True, nullable=False, index=True)
    invoice_date = Column(DateTime, nullable=False)
    reference_no = Column(String(100))
    note = Column(String(1000))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # Calculated totals
    total_excl = Column(Numeric(10, 2), default=0)
    total_tax = Column(Numeric(10, 2), default=0)
    total_incl = Column(Numeric(10, 2), default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="sales_orders")
    line_items = relationship("OrderLineItem", back_populates="sales_order", cascade="all, delete-orphan")


class OrderLineItem(Base):
    """Order line item entity with calculations"""
    __tablename__ = "order_line_items"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    note = Column(String(500))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    tax_rate = Column(Numeric(5, 2), nullable=False)  # Tax percentage 
    
    # Calculated amounts
    excl_amount = Column(Numeric(10, 2), nullable=False)  # Quantity * Price
    tax_amount = Column(Numeric(10, 2), nullable=False)   # Excl Amount * Tax Rate / 100
    incl_amount = Column(Numeric(10, 2), nullable=False)  # Excl Amount + Tax Amount

    # Relationships
    sales_order = relationship("SalesOrder", back_populates="line_items")
    item = relationship("Item", back_populates="order_line_items")
