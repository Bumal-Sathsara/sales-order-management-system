from abc import ABC, abstractmethod
from typing import List, Optional


class ICustomerRepository(ABC):
    """Interface for Customer repository"""
    
    @abstractmethod
    def get_all(self) -> List:
        pass
    
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[object]:
        pass
    
    @abstractmethod
    def create(self, customer: object) -> object:
        pass


class IItemRepository(ABC):
    """Interface for Item repository"""
    
    @abstractmethod
    def get_all(self) -> List:
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[object]:
        pass
    
    @abstractmethod
    def create(self, item: object) -> object:
        pass


class ISalesOrderRepository(ABC):
    """Interface for Sales Order repository"""
    
    @abstractmethod
    def get_all(self) -> List:
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[object]:
        pass
    
    @abstractmethod
    def create(self, order: object) -> object:
        pass
    
    @abstractmethod
    def update(self, order_id: int, order: object) -> Optional[object]:
        pass
    
    @abstractmethod
    def delete(self, order_id: int) -> bool:
        pass
