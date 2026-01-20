from celery import Celery
from app.core.worker import claim_job, process_job
import os

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "hashd",
    broker=broker_url
)

celery_app.conf.update(
    task_ignore_result=True,        # state lives in db
    task_acts_late=True,            # redeliver tasks
    worker_prefetch_multiplier=1,   # loadbalancing
)