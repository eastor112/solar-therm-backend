from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from schemas.locations import LocationResponseSchema


class WeatherSchema(BaseModel):
  id: int
  dhi: int
  temperature: float
  clearsky_dhi: int
  clearsky_dni: int
  clearsky_ghi: int
  dni: int
  ghi: int
  cloud_type: int
  relative_humidity: float
  solar_zenith_angle: float
  wind_direction: int
  wind_speed: float
  location_id: int
  date: datetime

  class Config:
    orm_mode = True
