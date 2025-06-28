from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from uuid import UUID

T = TypeVar("T")

class BaseRepositoryInterface(Generic[T], ABC):

    @abstractmethod
    def get_all(self) -> List[T]:
        ...

    @abstractmethod
    def get_by_id(self, item_id: UUID) -> T:
        ...
    
    @abstractmethod
    def add_item(self, item: T):
        ...

    @abstractmethod
    def delete_item(self, item_id: UUID):
        ...

    @abstractmethod
    def update_item(self, item_id: UUID, item: T) -> T:
        ...