from types import SimpleNamespace
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient
from pytest_mock import MockerFixture


@pytest.fixture
def app() -> Flask:
    from src.api import app

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def exam_dict() -> dict[str, Any]:
    return {
        "id": "EXAM-1011",
        "age": 25,
        "chest_pain_type": "ATA",
        "cholesterol": 289,
        "exercise_angina": "N",
        "fasting_bs": 0,
        "max_hr": 172,
        "oldpeak": 0.5,
        "resting_bp": 140,
        "resting_ecg": "Normal",
        "sex": "M",
        "st_slope": "Up",
    }


def cardio_report_task_mock(mocker: MockerFixture):
    mock_task = mocker.Mock()
    mock_task.id = "1"
    mock_task.result = None
    mocker.patch(
        "src.api.routes.create_cardio_report_task.delay", return_value=mock_task
    )


def mock_state_methods(mock_task: SimpleNamespace):
    def mock_successful():
        return mock_task.state == "SUCCESS"

    def mock_failed():
        return mock_task.state == "FAILURE"

    mock_task.successful = mock_successful
    mock_task.failed = mock_failed


def test_create_valid_cardio_report_task(
    client: FlaskClient, mocker: MockerFixture, exam_dict: dict[str, Any]
):
    cardio_report_task_mock(mocker)
    response = client.post(
        "/cardio_report_task",
        json=[exam_dict, exam_dict],
    )
    assert response.status_code == 201
    assert len(response.json) == 2
    assert response.json[0]["task_id"] == "1"
    assert response.json[1]["task_id"] == "1"


def test_create_invalid_cardio_report_task(
    client: FlaskClient, mocker: MockerFixture, exam_dict: dict[str, Any]
):
    cardio_report_task_mock(mocker)
    exam_dict["age"] = 17  # Invalid age
    response = client.post(
        "/cardio_report_task",
        json=[exam_dict, exam_dict],
    )
    assert response.status_code == 400
    assert len(response.json) == 2
    detail = {
        "ctx": {"gt": 18},
        "input": 17,
        "loc": [0, "age"],
        "msg": "Input should be greater than 18",
        "type": "greater_than",
        "url": "https://errors.pydantic.dev/2.10/v/greater_than",
    }
    assert response.json["details"][0] == detail
    detail["loc"] = [1, "age"]
    assert response.json["details"][1] == detail


def test_get_successful_cardio_report_task(client: FlaskClient, mocker: MockerFixture):
    mock_task = SimpleNamespace(
        id="id", state="SUCCESS", result="/app/data_path_report_file.html"
    )
    mock_state_methods(mock_task)
    mocker.patch("src.api.routes.AsyncResult", return_value=mock_task)
    response = client.get(f"/cardio_report_task/{mock_task.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {
        "result": mock_task.result,
        "status": mock_task.state,
        "task_id": mock_task.id,
    }


def test_get_failed_cardio_report_task(client: FlaskClient, mocker: MockerFixture):
    mock_task = SimpleNamespace(id="id", state="FAILURE", result="Failure reason")
    mock_state_methods(mock_task)
    mocker.patch("src.api.routes.AsyncResult", return_value=mock_task)
    response = client.get(f"/cardio_report_task/{mock_task.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {
        "result": mock_task.result,
        "status": mock_task.state,
        "task_id": mock_task.id,
    }


def test_get_pending_cardio_report_task(client: FlaskClient, mocker: MockerFixture):
    mock_task = SimpleNamespace(id="id", state="PENDING", result=None)
    mock_state_methods(mock_task)
    mocker.patch("src.api.routes.AsyncResult", return_value=mock_task)
    response = client.get(f"/cardio_report_task/{mock_task.id}")
    assert response.status_code == 404


def test_get_no_tasks_cardio_report_tasks(client: FlaskClient):
    response = client.post(
        "/get_cardio_report_tasks",
        json=[],
    )
    assert response.status_code == 400


def test_get_pending_cardio_report_tasks(client: FlaskClient, mocker: MockerFixture):
    mock_task = SimpleNamespace(id="id1", state="PENDING", result=None)
    mock_state_methods(mock_task)
    mocker.patch("src.api.routes.AsyncResult", return_value=mock_task)
    response = client.post("/get_cardio_report_tasks", json=[mock_task.id])
    assert response.status_code == 200
    tasks = response.json["tasks"]
    assert len(tasks) == 1
    assert tasks[0]["task_id"] == mock_task.id
    assert tasks[0]["status"] == mock_task.state


def test_get_valid_cardio_report_tasks(client: FlaskClient, mocker: MockerFixture):
    mock_task1 = SimpleNamespace(
        id="id1", state="SUCCESS", result="/app/data_path_report_file.html"
    )
    mock_state_methods(mock_task1)
    mock_task2 = SimpleNamespace(id="id2", state="FAILURE", result="failure reason")
    mock_state_methods(mock_task2)

    def side_effect(*args, **kwargs):
        # Return different mock objects for the first and second call
        return mock_task1 if args[0] == mock_task1.id else mock_task2

    mocker.patch("src.api.routes.AsyncResult", side_effect=side_effect)
    response = client.post(
        "/get_cardio_report_tasks",
        json=[mock_task1.id, mock_task2.id],
    )
    assert response.status_code == 200
    tasks = response.json["tasks"]
    assert len(tasks) == 2
    assert tasks[0]["task_id"] == mock_task1.id
    assert tasks[0]["status"] == mock_task1.state
    assert tasks[0]["result"] == mock_task1.result
    assert tasks[1]["task_id"] == mock_task2.id
    assert tasks[1]["status"] == mock_task2.state
    assert tasks[1]["result"] == mock_task2.result
