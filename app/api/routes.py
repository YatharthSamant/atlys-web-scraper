from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from ..core.schemas import ScrapeRequest
from ..scrapers.scraper_factory import ScraperFactory
from ..notifications.console_strategy import ConsoleNotification
from ..core.auth import token_required
from ..core.config import settings

router = APIRouter()
def verify_token(x_token: str = Header(...)):
    if x_token != settings.SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")



@router.post("/scrape", dependencies=[Depends(verify_token)])
async def scrape(request: ScrapeRequest):
    notifier = ConsoleNotification()
    scraper = ScraperFactory.get_scraper(num_pages=request.num_pages,
                                         proxy=request.proxy,
                                         scraper_type=request.scraper_type,
                                         storage_type=request.storage_type,
                                         notifier=notifier)
    scraper.scrape()
    return JSONResponse(content={"message": f"Scraped {len(scraper.products)} products."})