from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from backend.database import get_session
from schemas.theoric_params import TheoricParamsCreateSchema, TheoricParamsUpdateSchema
from services.theoric_params import TheoricParamsService

router = APIRouter(prefix='/tparams', tags=['theoric_params'])


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
