from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from datetime import datetime
from sqlalchemy import Boolean, Date
from sqlalchemy import Text

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(18, 2), nullable=False)
    status = Column(String, nullable=False)  # success / failed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    

class DailyReconciliationReport(Base):
    __tablename__ = "daily_reconciliation_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_date = Column(Date, unique=True, nullable=False)

    total_transactions = Column(Integer, nullable=False)
    successful_transactions = Column(Integer, nullable=False)
    failed_transactions = Column(Integer, nullable=False)
    total_volume = Column(Numeric(18, 2), nullable=False)

    anomaly_detected = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    

class JobRun(Base):
    __tablename__ = "job_runs"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # SUCCESS / FAILED

    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)

    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)