from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
)

from backend.database import get_session
from services.weather import WeatherService

router = APIRouter(prefix='/weather', tags=['weather'])


@router.get("")
async def getDayWeather(location_id: int, since: str, to: str, session: Session = Depends(get_session)):
  return WeatherService(session).get_day_weather(location_id, since, to)
