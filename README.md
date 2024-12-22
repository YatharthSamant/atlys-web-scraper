
# Atlys Web Scraper

This project is a Python-based web scraping tool using FastAPI to automate scraping information from the target website, [Dental Stall](https://dentalstall.com/shop/). The scraper fetches product details, including names, prices, and images, and supports configurable settings for the scraping process.

---

## Features

### Scraping
1. **Product Information Extraction**  
   - Scrapes product names, prices, and images directly from the catalogue pages.  
   - Avoids opening individual product cards for speed and efficiency.

2. **Configurable Settings**  
   - **Page Limit Setting**: Limits the number of catalogue pages to scrape.  
   - **Proxy Support**: Accepts a proxy string to route scraping requests.  

3. **Retry Mechanism**  
   - Retries failed page requests after a configurable delay, improving resilience against intermittent errors.

### Data Storage
- Scraped data is stored locally in JSON format:
  ```json
  [
    {
      "product_title": "",
      "product_price": 0,
      "path_to_image": ""
    }
  ]
  ```
- The tool is designed with flexibility to allow for easy integration with other storage solutions.

### Notifications
- Prints a scraping summary to the console, including:
  - Number of products scraped.
- The notification mechanism is modular, enabling future integration with other methods like email or messaging services.

### Data Integrity and Validation
- Implements type validation to ensure data accuracy and integrity during processing and storage.
- Caching via in-memory DB (e.g., Redis) to avoid redundant updates for unchanged product data.

### Security
- Supports static token-based authentication for scraping endpoints, adding a layer of access control.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YatharthSamant/atlys-web-scraper.git
   cd atlys-web-scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the FastAPI Server**  
   Start the FastAPI server locally:
   ```bash
   uvicorn run:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **API Endpoints**
   - **`/scrape`** (POST): Start a new scraping session. Accepts optional parameters:
     - `pages`: Number of pages to scrape.
     - `proxy`: Proxy string for request routing.
   - **Authentication**: Add a static token in the request header:
     ```text
     x-token: your_secure_token
     ```
   - **Curl**: Curl the hit the endpoint:
    ```
    curl --location 'http://127.0.0.1:8000/scrape' \
    --header 'Content-Type: application/json' \
    --header 'x-token: 24ed132eab2eaa675b4c7d49e23dbfc0468647ee3820e20fbbf71c684920fdf7' \
    --data '{
    "num_pages": 2,
    "proxy": "your_proxy_token"
    }' 
    ```

---

## Example Configuration

```json
{
  "pages": 5,
  "proxy": "http://my-proxy-server:8080"
}
```

---

## Output

### JSON Format
Data is saved locally in a JSON file in the following structure:
```json
[
  {
    "product_title": "Example Product",
    "product_price": 2450.00,
    "path_to_image": "/path/to/image.jpg"
  }
]
```

### Notifications
Sample console output after scraping:
```
Notification: Scraped and updated 48 products in the database.
```

---

## Design Overview

### Object-Oriented Structure
- **Classes**:
  - `Scraper`: Handles page parsing and data extraction.
  - `DataStore`: Manages data storage and validation.
  - `Notifier`: Sends notifications about the scraping process.
  - `CacheManager`: Implements caching for previously scraped results.

---

## Future Enhancements

1. **Database Integration**: Replace local JSON storage with a relational or NoSQL database.
2. **Advanced Authentication**: Implement OAuth or JWT-based authentication.
3. **Enhanced Notifications**: Add email or messaging service integration.
4. **Distributed Scraping**: Leverage a distributed framework like Celery for scalable scraping.
---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
