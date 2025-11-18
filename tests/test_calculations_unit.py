import pytest
from pydantic import ValidationError
from app.calculation_factory import get_operation
from app.schemas import CalculationType, CalculationCreate

def test_factory_add():
    op = get_operation(CalculationType.add, 2, 3)
    assert op.compute() == 5

def test_factory_sub():
    op = get_operation(CalculationType.sub, 5, 2)
    assert op.compute() == 3

def test_factory_mul():
    op = get_operation(CalculationType.mul, 3, 4)
    assert op.compute() == 12

def test_factory_div():
    op = get_operation(CalculationType.div, 10, 2)
    assert op.compute() == 5

def test_factory_invalid_type_raises():
    with pytest.raises(ValueError):
        get_operation("unknown", 1, 2)  # type: ignore[arg-type]

def test_division_by_zero_blocked():
    with pytest.raises(ValidationError):
        CalculationCreate(type=CalculationType.div, a=1, b=0)

def test_non_division_allows_zero_b():
    calc = CalculationCreate(type=CalculationType.mul, a=1, b=0)
    assert calc.b == 0
