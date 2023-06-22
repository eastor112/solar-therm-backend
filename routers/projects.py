from sqlalchemy.orm import Session
from backend.database import get_session
from schemas.projects import ProjectInitializeSchema
from services.projects import ProjectService
from fastapi import (
    APIRouter,
    Depends,
)


router = APIRouter(prefix='/projects', tags=['projects'])


@router.get("/")
async def get_projects(session: Session = Depends(get_session)):
  return ProjectService(session).get_projects()


@router.get("/{id}")
async def get_project(id: int, session: Session = Depends(get_session)):
  return ProjectService(session).get_project(id)


@router.post("/")
async def create_project(payload: ProjectInitializeSchema, session: Session = Depends(get_session)):
  return ProjectService(session).create_project(payload)
