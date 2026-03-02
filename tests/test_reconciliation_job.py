from datetime import date
from app.jobs.reconciliation import run_daily_reconciliation
from app.db.models import DailyReconciliationReport

def test_reconciliation_is_idempotent(db_session):
    # First run
    run_daily_reconciliation(db_session)

    # Second run (retry / duplicate execution)
    run_daily_reconciliation(db_session)

    reports = db_session.query(DailyReconciliationReport).all()

    assert len(reports) == 1
    assert reports[0].report_date == date.today()