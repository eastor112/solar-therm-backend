from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi import APIRouter, Depends, Body
from backend.database import get_session
from services.weather import WeatherService
from services.functions import fetch_pvgis_data
from schemas.weather import CalculateParams, PVGISParams

router = APIRouter(prefix='/weather', tags=['weather'])


@router.get("")
async def getDayWeather(location_id: int, since: str, to: str, session: Session = Depends(get_session)):
  return WeatherService(session).get_day_weather(location_id, since, to)


@router.post("/pvgis")
async def getDayWeather(params: PVGISParams = Body(...), session: Session = Depends(get_session)):

  year = int(params.date_time[:4])

  thermal_data = fetch_pvgis_data(
      params.latitud,
      params.longitud,
      "PVGIS-ERA5",
      year,
      year,
      int(params.inclinacion),
      params.azimuth,
      "json"
  )

  return thermal_data["outputs"]["hourly"]


@router.get("/test")
async def test(session: Session = Depends(get_session)):
  return WeatherService(session).test()


@router.post("/calculate")
async def calculate(params: CalculateParams = Body(...), session: Session = Depends(get_session)):
  year = int(params.date_time[:4])

  thermal_data = fetch_pvgis_data(
      params.latitud,
      params.longitud,
      "PVGIS-ERA5",
      year,
      year,
      int(params.inclinacion),
      params.azimuth,
      "json"
  )

  calculation_params = params.dict()
  calculation_params['thermal_data'] = thermal_data['outputs']['hourly']

  return WeatherService(session).calculate(calculation_params)
