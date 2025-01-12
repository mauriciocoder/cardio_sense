from flask import Request, Response, Blueprint, current_app as app, request, jsonify

from celery.result import AsyncResult
from ..worker import celery

from src.worker.tasks import create_cardio_report_task
from src.model.exams import CardioExam
from pydantic import ValidationError, TypeAdapter

bp = Blueprint("api", __name__)


def load_exams(request: Request) -> list[CardioExam]:
    return TypeAdapter(list[CardioExam]).validate_json(request.data)


@bp.route("/cardio_report", methods=["POST"])
def create_cardio_report() -> Response:
    try:
        exams = load_exams(request)
        result = []
        for i, exam in enumerate(exams):
            app.logger.info(f"Creating task for Exam #{i}: {exam}")
            task = create_cardio_report_task.delay(dict(exam))
            app.logger.info(f"Task #{task.id} created for Exam #{i}")
            result.append(
                {
                    "exam_iloc": i,
                    "task_id": task.id,
                }
            )
        return (
            jsonify(result),
            201,
        )
    except ValidationError as e:
        app.logger.error(e.errors())
        return jsonify({"error": "Invalid input data", "details": e.errors()}), 400


@bp.route("/cardio_report/<task_id>", methods=["GET"])
def get_cardio_report(task_id: str) -> Response:
    task = AsyncResult(task_id, app=celery)
    if task.state == "PENDING" and task.result is None:
        app.logger.warning(f"Task ID {task_id} not found.")
        return (
            jsonify({"task_id": task.id}),
            404,
        )
    if task.successful() or task.failed:
        return (
            jsonify(
                {
                    "task_id": task.id,
                    "result": task.result,
                }
            ),
            200,
        )
    return jsonify({"status": task.status}), 200
