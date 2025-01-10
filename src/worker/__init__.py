import os
import logging
from celery import Celery

celery = Celery(
    "worker",
    broker=os.environ.get("CELERY_BROKER_URL", "amqp://localhost"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "rpc://"),
)

logger = logging.getLogger("celery")
logger.setLevel(logging.INFO)
