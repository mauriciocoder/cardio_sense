from flasgger import swag_from
from flask import (
    abort,
    Request,
    Response,
    Blueprint,
    current_app as app,
    request,
    jsonify,
)

from celery.result import AsyncResult
from ..worker import celery

from src.worker.tasks import create_cardio_report_task
from src.model.exams import CardioExam
from pydantic import ValidationError, TypeAdapter

bp = Blueprint("api", __name__)


def load_exams(request: Request) -> list[CardioExam]:
    return TypeAdapter(list[CardioExam]).validate_json(request.data)


@bp.route("/cardio_report_task", methods=["POST"])
@swag_from("swag/cardio_report_task_swag.yml")
def cardio_report_task() -> Response:
    try:
        exams = load_exams(request)
        result = []
        for i, exam in enumerate(exams):
            app.logger.info(f"Creating task for Exam #{i}: {exam}")
            app.logger.info(f"Exam #{i}: {dict(exam)}")
            task = create_cardio_report_task.delay(dict(exam))
            app.logger.info(f"Task #{task.id} created for Exam #{i}")
            result.append(
                {
                    "exam_id": exam.id,
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


@bp.route("/cardio_report_task/<task_id>", methods=["GET"])
@swag_from("swag/cardio_report_task_get_swag.yml")
def get_cardio_report_task(task_id: str) -> Response:
    if not task_id:
        abort(404)
    task = AsyncResult(task_id, app=celery)
    if task.state == "PENDING" and task.result is None:
        app.logger.warning(f"Task ID {task_id} not found.")
        abort(404)
    response = {"status": task.state, "task_id": task.id}
    if task.successful() or task.failed():
        response["result"] = task.result
    return (
        jsonify(response),
        200,
    )


def validate_task_ids(task_ids: list[str]):
    if not isinstance(task_ids, list):
        raise ValueError("task_ids must be a list")
    if not task_ids:
        raise ValueError("task_ids cannot be an empty list")
    if not all(isinstance(task_id, str) for task_id in task_ids):
        raise ValueError("All task_ids must be strings")


@bp.route("/get_cardio_report_tasks", methods=["POST"])
@swag_from("swag/get_cardio_report_tasks_swag.yml")
def get_cardio_report_tasks() -> Response:
    task_ids = request.json
    try:
        validate_task_ids(task_ids)
    except ValueError as e:
        return jsonify({"error": "Invalid input data", "details": str(e)}), 400
    tasks = []
    for task_id in task_ids:
        task = AsyncResult(task_id, app=celery)
        app.logger.info(
            f"Task ID: {task.id}, Task State: {task.state}, Task Result: {task.result}"
        )
        response = {"status": task.state, "task_id": task.id}
        if task.successful() or task.failed():
            response["result"] = task.result
        tasks.append(response)
    return jsonify({"tasks": tasks}), 200
