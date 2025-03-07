from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_session
from schemas.theoric_register import TheoricRegisterCreateSchema, TheoricRegisterRetrieveSchema
from services.theoric_register import TheoricRegisterService
from typing import List


router = APIRouter(prefix='/register', tags=['theoric-registers'])


@router.post("/create-multiple")
async def create_theoric_registers(
    registers: List[TheoricRegisterCreateSchema],
    session: Session = Depends(get_session)
):
  return TheoricRegisterService().create_theoric_registers(session, registers)


@router.get("/{params_id}")
async def get_registers_by_params_id(
    params_id: int,
    session: Session = Depends(get_session)
) -> List[TheoricRegisterRetrieveSchema]:
  return TheoricRegisterService().get_registers_by_params_id(session, params_id)


@router.delete("/{params_id}")
async def delete_registers_by_params_id(
    params_id: int,
    session: Session = Depends(get_session)
):
  deleted_count = TheoricRegisterService(
  ).delete_registers_by_params_id(session, params_id)
  return {"message": f"Successfully deleted {deleted_count} theoric registers."}


@router.get("/project/{project_id}", response_model=List[List[TheoricRegisterRetrieveSchema]])
async def get_registers_grouped_by_project(
    project_id: int,
    session: Session = Depends(get_session)
):
  grouped_registers = TheoricRegisterService(
  ).get_registers_grouped_by_project(session, project_id)
  return grouped_registers
