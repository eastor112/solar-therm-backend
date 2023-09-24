from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
)
from backend.database import get_session
from models.theoric_params import TheoricParams
from schemas.theoric_params import EnergyCalculatorRequestSchema, TheoricParamsCreateSchema, TheoricParamsUpdateSchema
from services.theoric_params import TheoricParamsService
from thermal_model.pipeline_energy_anual import calculate_annual_energy

router = APIRouter(prefix='/theoretical', tags=['theoric_params'])


@router.get("")
async def get_all_theoric_params(session: Session = Depends(get_session)):
  return TheoricParamsService(session).get_all_theoric_params()


@router.get("/{theoric_param_id}")
async def get_theoric_param(theoric_param_id: int, session: Session = Depends(get_session)):
  theoric_param = TheoricParamsService(
      session).get_theoric_param(theoric_param_id)
  if not theoric_param:
    raise HTTPException(status_code=404, detail="TheoricParam not found")
  return theoric_param


@router.post("")
async def create_theoric_param(payload: TheoricParamsCreateSchema, session: Session = Depends(get_session)):
  return TheoricParamsService(session).create_theoric_param(payload)


@router.patch("/{theoric_param_id}")
async def update_theoric_param(theoric_param_id: int, payload: TheoricParamsUpdateSchema, session: Session = Depends(get_session)):
  theoric_param = TheoricParamsService(
      session).update_theoric_param(theoric_param_id, payload)
  if not theoric_param:
    raise HTTPException(status_code=404, detail="TheoricParam not found")
  return theoric_param


@router.delete("/{theoric_param_id}")
async def delete_theoric_param(theoric_param_id: int, session: Session = Depends(get_session)):
  if not TheoricParamsService(session).delete_theoric_param(theoric_param_id):
    raise HTTPException(status_code=404, detail="TheoricParam not found")
  return {"message": "TheoricParam deleted successfully"}


@router.post("/calculate")
async def calculate_energy(
    request_data: EnergyCalculatorRequestSchema,
    session: Session = Depends(get_session)
):
  return TheoricParamsService(session).calculate_annual_energy(request_data)


@router.get("/calculate/params/{theoric_param_id}")
async def calculate_energy_for_location_pipeline(
    theoric_param_id: int = Path(..., title="Theoric Param ID"),
    session: Session = Depends(get_session)
):

  return TheoricParamsService(
      session).calculate_annual_energy_from_params(theoric_param_id)
