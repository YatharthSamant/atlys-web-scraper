import os
import json
from typing import List
from ..models.products import Product
from .storage_strategy import StorageStrategy
import redis

class JSONStorage(StorageStrategy):
    def __init__(self):
        self.json_path = os.path.join(os.path.dirname(__file__), 'products.json')
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.ttl = 3600 
    
    def load_cache(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def load_redis_cache(self):
        redis_keys = self.redis_client.keys()
        redis_data = {}
        for key in redis_keys:
            cached_product = self.redis_client.get(key)
            if cached_product:
                redis_data[key.decode('utf-8')] = json.loads(cached_product)
        return redis_data

    def save_products(self, products: List[Product]):
        existing_data = self.load_cache()
        redis_data = self.load_redis_cache()

        for product in products:
            product_dict = product.dict()
            redis_product = redis_data.get(product.product_title)
            if redis_product:
                if redis_product['product_price'] == product.product_price:
                    continue  # Skip if the price remains the same
                elif redis_product['product_price'] < product.product_price:
                    existing_data[product.product_title] = product_dict  # Update if the price has increased
            else:
                existing_data[product.product_title] = product_dict  # Add new entry if the product does not exist

        with open(self.json_path, 'w') as f:
            json.dump(existing_data, f, indent=4)

        # Update the cache
        self.cache = existing_data

    def is_product_updated(self, product: Product) -> bool:
        cached_product = self.redis_client.get(product.product_title)
        if cached_product:
            cached_product = json.loads(cached_product)
            if cached_product['product_price'] == product.product_price:
                return False
        self.redis_client.set(product.product_title, json.dumps(product.dict()), ex=self.ttl)
        return True