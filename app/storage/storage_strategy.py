from abc import ABC, abstractmethod
from typing import List
from ..models.products import Product

class StorageStrategy(ABC):
    @abstractmethod
    def save_products(self, products: List[Product]):
        pass

    @abstractmethod
    def is_product_updated(self, product: Product) -> bool:
        pass