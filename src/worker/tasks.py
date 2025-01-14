import inspect
import os

from celery import current_task

from . import celery, logger
from jinja2 import Template

from src.model.exams import CardioExam
from src.worker.cardio_report_template import cardio_report_template
from src.worker.llm import LLM


@celery.task(bind=True, max_retries=3, default_retry_delay=90)
def create_cardio_report_task(self, exam_dict: dict) -> str:
    try:
        logger.info(f"Creating report for exam: {exam_dict}")
        report_content = create_cardio_report_content(CardioExam(**exam_dict))
        report_path = save_report(report_content)
        return report_path
    except Exception as e:
        logger.error(f"Failed to create report for exam: {exam_dict}. Error: {e}")
        self.retry(exc=e)


def create_cardio_report_content(exam: CardioExam) -> str:
    template = Template(cardio_report_template)
    report_content = template.render(
        **dict(inspect.getmembers(exam)),
        summary=LLM().create_cardio_report_summary(exam),
    )
    return report_content


def save_report(report: str) -> str:
    task_id = current_task.request.id
    report_path = (
        os.environ.get("CARDIO_SENSE_DATA_PATH") + f"cardio_report_{task_id}.html"
    )
    logger.info(f"Saving report to {report_path}")
    with open(report_path, "w") as f:
        f.write(report)
    logger.info(f"Report saved to {report_path}")
    return report_path
