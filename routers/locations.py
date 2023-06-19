from typing import List
from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
)

from backend.database import get_session
from services.locations import LocationsService

router = APIRouter(prefix='/locations', tags=['locations'])


@router.get("/")
async def get_locations(session: Session = Depends(get_session)):
  return LocationsService(session).get_locations()
