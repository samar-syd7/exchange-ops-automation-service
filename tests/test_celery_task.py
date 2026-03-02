from app.tasks.reconciliation import daily_reconciliation_task

def test_celery_task_executes_logic():
    # This ensures the task is callable and wired
    result = daily_reconciliation_task.run()
    assert result is None