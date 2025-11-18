from sqlalchemy.orm import Session
from . import models, schemas
from .calculation_factory import get_operation

def create_calculation(db: Session, calc_in: schemas.CalculationCreate, user_id: int | None = None) -> models.Calculation:
    operation = get_operation(calc_in.type, calc_in.a, calc_in.b)
    result = operation.compute()
    db_calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type.value,
        result=result,
        user_id=user_id,
    )
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc

def get_calculation(db: Session, calc_id: int) -> models.Calculation | None:
    return db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
