import pytest
from src.model.exams import CardioExam
from pydantic import ValidationError


def test_valid_cardio_exam():
    exam = CardioExam(
        age=25,
        sex="M",
        chest_pain_type="ATA",
        resting_bp=140,
        cholesterol=289,
        fasting_bs=0,
        resting_ecg="Normal",
        max_hr=172,
        exercise_angina="N",
        oldpeak=0.5,
        st_slope="Up",
    )
    assert exam


def test_invalid_age_below_lower_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=17,  # Invalid age, below 18
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_age_above_upper_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=101,  # Invalid age, above 100
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_resting_bp_below_lower_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=85,  # Invalid resting BP, below 90
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_resting_bp_above_upper_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=205,  # Invalid resting BP, above 200
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_cholesterol_below_lower_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=100,  # Invalid cholesterol, below 150
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_cholesterol_above_upper_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=350,  # Invalid cholesterol, above 300
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_fasting_bs_below_lower_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=-1,  # Invalid fasting BS, below 0
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_fasting_bs_above_upper_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=2,  # Invalid fasting BS, above 1
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_max_hr_below_lower_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=40,  # Invalid max HR, below 50
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_max_hr_above_upper_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=230,  # Invalid max HR, above 220
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_oldpeak_below_lower_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=-1,  # Invalid oldpeak, below 0
            st_slope="Up",
        )


def test_invalid_oldpeak_above_upper_bound():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=7,  # Invalid oldpeak, above 6
            st_slope="Up",
        )


def test_invalid_sex_invalid_pattern():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="X",  # Invalid sex, must be "M" or "F"
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_chest_pain_type_invalid_pattern():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="XYZ",  # Invalid chest_pain_type
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_resting_ecg_invalid_pattern():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Abnormal",  # must be one of Normal, ST, or LVH
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_exercise_angina_invalid_pattern():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="Maybe",  # Invalid exercise_angina, must be "Y" or "N"
            oldpeak=0.5,
            st_slope="Up",
        )


def test_invalid_st_slope_invalid_pattern():
    with pytest.raises(ValidationError):
        CardioExam(
            age=25,
            sex="M",
            chest_pain_type="ATA",
            resting_bp=140,
            cholesterol=289,
            fasting_bs=0,
            resting_ecg="Normal",
            max_hr=172,
            exercise_angina="N",
            oldpeak=0.5,
            st_slope="Steep",  # Invalid st_slope, must be one of Up, Flat, or Down
        )
