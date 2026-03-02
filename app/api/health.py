import logging
from datetime import datetime, date, time, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db.models import JobRun, DailyReconciliationReport
from app.schemas.health import HealthResponse
from sqlalchemy import text

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    
    try:
        db.execute(text("SELECT 1"))
        database_ok = True
    except Exception:
        logger.critical("Database connectivity check failed", exc_info=True)
        database_ok = False

    
    last_successful_job = (
        db.query(JobRun)
        .filter(
            JobRun.job_name == "daily_reconciliation",
            JobRun.status == "SUCCESS"
        )
        .order_by(JobRun.finished_at.desc())
        .first()
    )

    
    today_report = (
        db.query(DailyReconciliationReport)
        .filter(
            DailyReconciliationReport.report_date == date.today()
        )
        .first()
    )

    
    now = datetime.utcnow()
    today_midnight = datetime.combine(date.today(), time.min)

    missed_daily_reconciliation = (
        now > today_midnight + timedelta(hours=1)  # grace window
        and not today_report
    )

    overall_status = "ok" if database_ok else "degraded"

    return HealthResponse(
        status=overall_status,
        database=database_ok,
        last_successful_job_run=(
            last_successful_job.finished_at
            if last_successful_job else None
        ),
        today_reconciliation_present=bool(today_report),
        missed_daily_reconciliation=missed_daily_reconciliation,
    )