from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(calc_in: schemas.CalculationCreate, db: Session = Depends(get_db), user_id: Optional[int] = None):
    try:
        db_calc = crud.create_calculation(db, calc_in, user_id=user_id)
        return db_calc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    db_calc = crud.get_calculation(db, calc_id)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return db_calc
