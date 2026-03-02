import logging
from celery import shared_task

from app.celery_app import celery_app
from app.db.base import SessionLocal
from app.jobs.reconciliation import run_daily_reconciliation

logger = logging.getLogger(__name__)

@celery_app.task(
    name="tasks.daily_reconciliation",
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 30},
    retry_backoff=True,
)
def daily_reconciliation_task(self):
    """
    Celery task wrapper for the daily reconciliation job.
    """

    logger.info("Celery task started: daily_reconciliation")

    db = SessionLocal()
    try:
        run_daily_reconciliation(db)
    except Exception as exc:
        logger.critical(
            "Celery reconciliation task failed",
            exc_info=True
        )
        raise exc
    finally:
        db.close()