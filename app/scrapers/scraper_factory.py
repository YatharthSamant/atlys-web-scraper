from .dental_scraper import DentalStallScraper 
from ..core.config import settings
from ..storage.json_storage import JSONStorage
from ..notifications.notification_strategy import NotificationStrategy

class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_type: str, storage_type: str, num_pages: int, proxy: str, notifier: NotificationStrategy = None):
        if storage_type == 'json':
            storage = JSONStorage()
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

        if scraper_type == 'dental_stall':
            return DentalStallScraper(num_pages=num_pages,
                                      proxy=proxy,
                                      storage=storage,
                                      notifier=notifier)
        else:
            raise ValueError(f"Unknown scraper type: {scraper_type}")