import requests
from bs4 import BeautifulSoup
from ..models.products import Product
from ..core.config import settings
from ..notifications.notification_strategy import NotificationStrategy
from ..notifications.console_strategy import ConsoleNotification
from ..storage.storage_strategy import StorageStrategy
import os
import time
from typing import List, Optional
import uuid

class DentalStallScraper:
    def __init__(self, num_pages: int = settings.NUM_PAGES, proxy: Optional[str] = settings.PROXY, notifier: Optional[NotificationStrategy] = None, storage: Optional[StorageStrategy] = None):
        self.num_pages = num_pages
        self.proxy = proxy
        self.base_url = "https://dentalstall.com/shop/"
        self.products: List[Product] = []
        self.image_dir = os.path.join(os.path.dirname(__file__), 'images')
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        self.notifier = notifier or ConsoleNotification()
        self.storage = storage

    def scrape(self):
        for page in range(1, self.num_pages + 1):
            url = f"{self.base_url}/page/{page}"
            try:
                response = self.fetch_page(url)
                self.parse_page(response.text)
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                time.sleep(settings.RETRY_DELAY)
                continue
        self.storage.save_products(self.products)
        self.notify()

    def fetch_page(self, url: str) -> requests.Response:
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        response = requests.get(url)
        response.raise_for_status()
        return response

    def parse_page(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        product_elements = soup.select(".product-inner.clearfix")
        for element in product_elements:
            title = element.select_one('.mf-product-thumbnail').find('img').get('alt').strip()
            price = float(element.select_one('bdi').text.strip().replace('₹', ''))
            image_url = element.select_one('.mf-product-thumbnail').select_one('a').get('href')
            image_path = self.download_image(image_url)
            product = Product(product_title=title, product_price=price, path_to_image=image_path)
            if not self.storage.is_product_updated(product):
                self.products.append(product)


    def download_image(self, url: str) -> str:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = os.path.basename(url)
            if not image_name or image_name == '/':
                image_name = f"image_{uuid.uuid4()}.jpg"  # Use UUID for unique name
            else:
                # Add UUID to the original image name to ensure uniqueness
                name, ext = os.path.splitext(image_name)
                image_name = f"{name}_{uuid.uuid4()}{ext}"
            image_path = os.path.join(self.image_dir, image_name)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return image_path
        else:
            raise Exception(f"Failed to download image from {url}")

    def notify(self):
        message = f"Notification: Scraped and updated {len(self.products)} products in the database."
        self.notifier.notify(message)