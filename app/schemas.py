from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator, ValidationInfo


class CalculationType(str, Enum):
    add = "add"
    sub = "sub"
    mul = "mul"
    div = "div"


class CalculationCreate(BaseModel):
    type: CalculationType
    a: float
    b: float

    @field_validator("b")
    @classmethod
    def no_zero_divisor(cls, v: float, info: ValidationInfo) -> float:
        data = info.data or {}
        calc_type = data.get("type")
        if calc_type == CalculationType.div and v == 0:
            raise ValueError("b cannot be zero for division")
        return v


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: float
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
