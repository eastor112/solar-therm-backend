from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from backend.database import get_session
from schemas.pipelines import PipelineCreateSchema, PipelineUpdateSchema
from services.pipelines import PipelineService

router = APIRouter(prefix='/pipelines', tags=['pipelines'])


@router.post("")
async def create_pipeline(payload: PipelineCreateSchema, session: Session = Depends(get_session)):
  return PipelineService(session).create_pipeline(payload)


@router.get("")
async def get_pipelines(session: Session = Depends(get_session)):
  return PipelineService(session).get_pipelines()


@router.get("/{id}")
async def get_pipeline(id: int, session: Session = Depends(get_session)):
  pipeline = PipelineService(session).get_pipeline(id)
  if not pipeline:
    raise HTTPException(status_code=404, detail="Pipeline not found")
  return pipeline


@router.patch("/{id}")
async def update_pipeline(id: int, payload: PipelineUpdateSchema, session: Session = Depends(get_session)):
  pipeline = PipelineService(session).update_pipeline(id, payload)
  if not pipeline:
    raise HTTPException(status_code=404, detail="Pipeline not found")
  return pipeline


@router.delete("/{id}")
async def delete_pipeline(id: int, session: Session = Depends(get_session)):
  if not PipelineService(session).delete_pipeline(id):
    raise HTTPException(status_code=404, detail="Pipeline not found")
  return {"message": "Pipeline deleted successfully"}
