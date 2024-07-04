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


class PVGISParams(BaseModel):
  latitude: float
  longitude: float
  raddatabase: str = "PVGIS-ERA5"
  startyear: int = 2020
  endyear: int = 2020
  angle: int = 15
  azimuth: int = 0
  outputformat: str = 'json'


class CalculateParams(BaseModel):
  date_time: str
  latitud_local: float
  longitud_local: float
  altitud_local: float
  inclinacion: float
  azimuth: int
  t_amb: float
  v_viento: float
  d_int: float
  d_ext: float
  lon_tubo: float
  s_sep: float
  vol_tank: float
  num_tubos: int
  e_tank: float
  e_aisl: float
  e_cub: float
  tau_glass: float
  alfa_glass: float
  h_int: float
  h_ext: float
  k_tank: float
  k_aisl: float
  k_cub: float
  f_flujo: float
  beta_coef: float
  nn: int
  n_div: int
