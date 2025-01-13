import os
import logging
from celery import Celery

celery = Celery(
    "worker",
    broker=os.environ.get("CELERY_BROKER_URL", "amqp://rabbitmq"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "rpc://"),
    result_persistent=True,
    task_track_started=True,
)

logger = logging.getLogger("celery")
logger.setLevel(logging.INFO)
