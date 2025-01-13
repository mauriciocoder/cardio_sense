from typing import Any

import pytest
from src.model.exams import CardioExam
from pydantic import ValidationError


@pytest.fixture
def exam_dict() -> dict[str, Any]:
    exam = {
        "id": "ID",
        "age": 25,
        "sex": "M",
        "chest_pain_type": "ATA",
        "resting_bp": 140,
        "cholesterol": 289,
        "fasting_bs": 0,
        "resting_ecg": "Normal",
        "max_hr": 172,
        "exercise_angina": "N",
        "oldpeak": 0.5,
        "st_slope": "Up",
    }
    yield exam


def assert_error(exam_dict):
    with pytest.raises(ValidationError):
        CardioExam(**exam_dict)


def test_valid_cardio_exam(exam_dict: dict[str, Any]):
    exam = CardioExam(**exam_dict)
    assert exam


def test_invalid_id(exam_dict: dict[str, Any]):
    exam_dict["id"] = None  # Id is not optional
    assert_error(exam_dict)


def test_invalid_age_below_lower_bound(exam_dict: dict[str, Any]):
    exam_dict["age"] = 17  # Invalid age, below 18
    assert_error(exam_dict)


def test_invalid_age_above_upper_bound(exam_dict: dict[str, Any]):
    exam_dict["age"] = 101  # Invalid age, above 100
    assert_error(exam_dict)


def test_invalid_resting_bp_below_lower_bound(exam_dict: dict[str, Any]):
    exam_dict["resting_bp"] = 85  # Invalid resting BP, below 90
    assert_error(exam_dict)


def test_invalid_resting_bp_above_upper_bound(exam_dict: dict[str, Any]):
    exam_dict["resting_bp"] = 205  # Invalid resting BP, above 200
    assert_error(exam_dict)


def test_invalid_cholesterol_below_lower_bound(exam_dict: dict[str, Any]):
    exam_dict["cholesterol"] = 100  # Invalid cholesterol, below 150
    assert_error(exam_dict)


def test_invalid_cholesterol_above_upper_bound(exam_dict: dict[str, Any]):
    exam_dict["cholesterol"] = 350  # Invalid cholesterol, above 300
    assert_error(exam_dict)


def test_invalid_fasting_bs_below_lower_bound(exam_dict: dict[str, Any]):
    exam_dict["fasting_bs"] = -1  # Invalid fasting BS, below 0
    assert_error(exam_dict)


def test_invalid_fasting_bs_above_upper_bound(exam_dict: dict[str, Any]):
    exam_dict["fasting_bs"] = 2  # Invalid fasting BS, above 1
    assert_error(exam_dict)


def test_invalid_max_hr_below_lower_bound(exam_dict: dict[str, Any]):
    exam_dict["max_hr"] = 40  # Invalid max HR, below 50
    assert_error(exam_dict)


def test_invalid_max_hr_above_upper_bound(exam_dict: dict[str, Any]):
    exam_dict["max_hr"] = 230  # Invalid max HR, above 220
    assert_error(exam_dict)


def test_invalid_oldpeak_below_lower_bound(exam_dict: dict[str, Any]):
    exam_dict["oldpeak"] = -1  # Invalid oldpeak, below 0
    assert_error(exam_dict)


def test_invalid_oldpeak_above_upper_bound(exam_dict: dict[str, Any]):
    exam_dict["oldpeak"] = 7  # Invalid oldpeak, above 6
    assert_error(exam_dict)


def test_invalid_sex_invalid_pattern(exam_dict: dict[str, Any]):
    exam_dict["sex"] = "X"  # Invalid sex, must be "M" or "F"
    assert_error(exam_dict)


def test_invalid_chest_pain_type_invalid_pattern(exam_dict: dict[str, Any]):
    exam_dict["chest_pain_type"] = "XYZ"  # Invalid chest_pain_type
    assert_error(exam_dict)


def test_invalid_resting_ecg_invalid_pattern(exam_dict: dict[str, Any]):
    exam_dict["resting_ecg"] = "Abnormal"  # must be one of Normal, ST, or LVH
    assert_error(exam_dict)


def test_invalid_exercise_angina_invalid_pattern(exam_dict: dict[str, Any]):
    exam_dict[
        "exercise_angina"
    ] = "Maybe"  # Invalid exercise_angina, must be "Y" or "N"
    assert_error(exam_dict)


def test_invalid_st_slope_invalid_pattern(exam_dict: dict[str, Any]):
    exam_dict[
        "st_slope"
    ] = "Steep"  # Invalid st_slope, must be one of Up, Flat, or Down
    assert_error(exam_dict)
