from sqlalchemy.orm import Session
from backend.database import get_session
from schemas.projects import ProjectInitializeSchema, ProjectUpdateSchema
from services.projects import ProjectService
from fastapi import (
    APIRouter,
    Depends,
    Query,
)


router = APIRouter(prefix='/projects', tags=['projects'])


@router.get("/")
async def get_projects(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1),
    filter: str = Query(default=None),
    session: Session = Depends(get_session)
):
  return ProjectService(session).get_projects(page=page, size=size, filter_param=filter)


@router.get("/{id}")
async def get_project(id: int, session: Session = Depends(get_session)):
  return ProjectService(session).get_project(id)


@router.post("/")
async def create_project(payload: ProjectInitializeSchema, session: Session = Depends(get_session)):
  return ProjectService(session).create_project(payload)


@router.patch("/{id}")
async def update_project(id: int, payload: ProjectUpdateSchema, session: Session = Depends(get_session)):
  return ProjectService(session).update_project(id, payload)


@router.delete("/{id}")
async def delete_project(id: int, session: Session = Depends(get_session)):
  return ProjectService(session).delete_project(id)
