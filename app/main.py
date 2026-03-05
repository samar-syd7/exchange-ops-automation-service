from fastapi import FastAPI
import logging

from app.core.logging import setup_logging
from app.core.config import settings
from app.db.base import engine
from app.db.models import Base
from app.api.health import router as health_router
from app.core.scheduler import start_scheduler, scheduler


# Logging

setup_logging()
logger = logging.getLogger(__name__)


# App

app = FastAPI(
    title="Exchange Ops Automation Service",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"status": "ok"}


# Lifecycle

@app.on_event("startup")
def on_startup():
    logger.info("Starting Exchange Ops Automation Service")

    Base.metadata.create_all(bind=engine)

    if settings.ENABLE_SCHEDULER:
        start_scheduler()
    else:
        logger.info("Scheduler disabled by configuration")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down scheduler")
    if scheduler.running:
        scheduler.shutdown()


# Routes

app.include_router(health_router, prefix="/api")