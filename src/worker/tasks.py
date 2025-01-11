from . import celery, logger
from jinja2 import Template

from src.model.exams import CardioExam


@celery.task
def create_cardio_report_task(exam_dict: dict):
    logger.info(f"Creating report for exam: {exam_dict}")
    exam = CardioExam(**exam_dict)
    template = Template(
        """
    <html>
        <body>
            <h1>Cholesterol Report</h1>
            <p><strong>Age:</strong> {{ age }}</p>
            <p><strong>Gender:</strong> {{ gender }}</p>
        </body>
    </html>
    """
    )
    report = template.render(age=exam.age, gender=exam.sex)
    return report
