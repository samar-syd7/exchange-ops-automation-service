import logging
from datetime import datetime, timedelta, date

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.db.models import (
    Transaction,
    DailyReconciliationReport,
    JobRun
)

logger = logging.getLogger(__name__)

def run_daily_reconciliation(db: Session):
    job_run = JobRun(
        job_name="daily_reconciliation",
        status="RUNNING",
        started_at=datetime.utcnow()
    )
    db.add(job_run)
    db.commit()
    db.refresh(job_run)

    try:
        today = date.today()
        start_time = datetime.utcnow() - timedelta(days=1)

        transactions = (
            db.query(Transaction)
            .filter(Transaction.created_at >= start_time)
            .all()
        )

        total_transactions = len(transactions)
        successful_transactions = sum(
            1 for tx in transactions if tx.status == "success"
        )
        failed_transactions = total_transactions - successful_transactions

        total_volume = sum(
            float(tx.amount) for tx in transactions
        )

        anomaly_detected = total_transactions == 0
        
        existing_report = (
            db.query(DailyReconciliationReport)
            .filter(DailyReconciliationReport.report_date == today)
            .first()
        )

        if existing_report:
            logger.info(
                "Daily reconciliation already exists for %s, skipping job",
                today
            )

            job_run.status = "SUCCESS"
            job_run.finished_at = datetime.utcnow()
            db.commit()
            return

        report = DailyReconciliationReport(
            report_date=today,
            total_transactions=total_transactions,
            successful_transactions=successful_transactions,
            failed_transactions=failed_transactions,
            total_volume=total_volume,
            anomaly_detected=anomaly_detected
        )

        db.add(report)

        job_run.status = "SUCCESS"
        job_run.finished_at = datetime.utcnow()

        if anomaly_detected:
            logger.critical(
                "Daily reconciliation anomaly detected: zero transactions in last 24h"
            )
        else:
            logger.info(
                "Daily reconciliation completed successfully: %s transactions",
                total_transactions
            )

        db.commit()

    except Exception as exc:
        db.rollback()

        job_run.status = "FAILED"
        job_run.finished_at = datetime.utcnow()
        job_run.error_message = str(exc)

        db.add(job_run)
        db.commit()

        logger.critical(
            "Daily reconciliation job failed",
            exc_info=True
        )

        raise
    
def run_reconciliation_once(db: Session):
    logger.info("Manually triggering daily reconciliation job")
    run_daily_reconciliation(db)