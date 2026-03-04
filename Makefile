install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

worker:
	celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo

test:
	pytest -v
