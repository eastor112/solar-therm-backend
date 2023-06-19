from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
)

from backend.database import get_session
from schemas.locations import LocationCreateSchema
from services.locations import LocationsService

router = APIRouter(prefix='/locations', tags=['locations'])


@router.get("/")
async def get_locations(session: Session = Depends(get_session)):
  return LocationsService(session).get_locations()


@router.get("/{id}")
async def get_locations(id: int, session: Session = Depends(get_session)):
  return LocationsService(session).get_location(id)


@router.post("/")
async def create_location(payload: LocationCreateSchema, session: Session = Depends(get_session)):
  return LocationsService(session).create_location(payload)
