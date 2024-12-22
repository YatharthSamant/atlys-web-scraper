import redis

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.ttl = 3600 

    def get_product_price(self, product_title: str) -> Optional[float]:
        cached_data = self.redis_client.get(f"product:{product_title}")
        if cached_data:
            return float(cached_data)
        return None
    
    def set_product_price(self, product_title: str, price: float) -> None:
        self.redis_client.set(f"product:{product_title}", str(price))