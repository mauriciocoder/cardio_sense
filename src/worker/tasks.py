import inspect
import os

from celery import current_task

from . import celery, logger
from jinja2 import Template

from src.model.exams import CardioExam
from static.cardio_report_template import cardio_report_template
from src.worker.llm import LLM


@celery.task
def create_cardio_report_task(exam_dict: dict):
    logger.info(f"Creating report for exam: {exam_dict}")
    exam = CardioExam(**exam_dict)
    template = Template(cardio_report_template)
    report_content = template.render(
        **dict(inspect.getmembers(exam)),
        summary=LLM().create_cardio_report_summary(exam),
    )
    report_path = save_report(report_content)
    return report_path, report_content


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
