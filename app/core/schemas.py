from pydantic import BaseModel

class ScrapeRequest(BaseModel):
    num_pages: int = 5
    proxy: str = None
    scraper_type: str = 'dental_stall'
    storage_type: str = 'json'