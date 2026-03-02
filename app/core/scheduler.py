import logging
from apscheduler.schedulers.background import BackgroundScheduler

from app.db.base import SessionLocal
from app.jobs.reconciliation import run_daily_reconciliation

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def scheduled_reconciliation_job():
    logger.info("Scheduled daily reconciliation job triggered")

    db = SessionLocal()
    try:
        run_daily_reconciliation(db)
    finally:
        db.close()


def start_scheduler():
    # prevent double start 
    if scheduler.running:
        logger.info("Scheduler already running, skipping start")
        return

    scheduler.add_job(
        scheduled_reconciliation_job,
        trigger="cron",
        hour=0,
        minute=0,
        id="daily_reconciliation_job",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler started")