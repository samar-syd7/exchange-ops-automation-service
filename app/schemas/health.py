from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class HealthResponse(BaseModel):
    status: str
    database: bool
    last_successful_job_run: Optional[datetime]
    today_reconciliation_present: bool
    missed_daily_reconciliation: bool