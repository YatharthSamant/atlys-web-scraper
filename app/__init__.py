from fastapi import FastAPI
from .core.config import settings
from .api.routes import router

def create_app():
    app = FastAPI()
    app.include_router(router)
    return app