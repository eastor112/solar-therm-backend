from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from backend.database import get_session
from schemas.locations import LocationCreateSchema, LocationUpdateSchema
from services.locations import LocationsService

router = APIRouter(prefix='/locations', tags=['locations'])


@router.get("")
async def get_locations(session: Session = Depends(get_session)):
  return LocationsService(session).get_locations()


@router.get("/{id}")
async def get_locations(id: int, session: Session = Depends(get_session)):
  return LocationsService(session).get_location(id)


@router.post("")
async def create_location(payload: LocationCreateSchema, session: Session = Depends(get_session)):
  return LocationsService(session).create_location(payload)


@router.patch("/{id}")
async def update_location(id: int, payload: LocationUpdateSchema, session: Session = Depends(get_session)):
  location = LocationsService(session).update_location(id, payload)
  if not location:
    raise HTTPException(status_code=404, detail="Location not found")
  return location


@router.delete("/{id}")
async def delete_location(id: int, session: Session = Depends(get_session)):
  if not LocationsService(session).delete_location(id):
    raise HTTPException(status_code=404, detail="Location not found")
  return {"message": "Location deleted successfully"}
