from pydantic import BaseModel, Field
from typing import Annotated
from pydantic import StringConstraints


class CardioExam(BaseModel):
    age: Annotated[int, Field(strict=True, gt=18, le=100)]
    sex: Annotated[
        str, StringConstraints(strip_whitespace=True, to_upper=True, pattern=r"^(M|F)$")
    ]
    chest_pain_type: Annotated[str, StringConstraints(pattern=r"^(ATA|NAP|ASY|TA)$")]
    resting_bp: Annotated[int, Field(ge=90, le=200)]
    cholesterol: Annotated[int, Field(ge=150, le=300)]
    fasting_bs: Annotated[int, Field(ge=0, le=1)]
    resting_ecg: Annotated[str, StringConstraints(pattern=r"^(Normal|ST|LVH)$")]
    max_hr: Annotated[int, Field(ge=50, le=220)]
    exercise_angina: Annotated[str, StringConstraints(pattern=r"^(Y|N)$")]
    oldpeak: Annotated[float, Field(ge=0, le=6)]
    st_slope: Annotated[str, StringConstraints(pattern=r"^(Up|Flat|Down)$")]
