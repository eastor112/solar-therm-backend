from datetime import datetime
from sqlalchemy import and_
from models.weather import Weather
from schemas.weather import WeatherSchema
import requests
from fastapi import HTTPException
from functools import lru_cache
from thermal_model.results import calcular_parametros_solares
import json
import numpy as np

from services.base import (
    BaseService,
)


@lru_cache(maxsize=32)
def fetch_pvgis_data(
    lat: float,
    lon: float,
    raddatabase: str,
    startyear: int,
    endyear: int,
    angle: int,
    azimuth: int,
    outputformat: str
):
  params = {
      "lat": lat,
      "lon": lon,
      "raddatabase": raddatabase,
      "endyear": endyear,
      "startyear": startyear,
      "angle": angle,
      "aspect": azimuth,
      "outputformat": outputformat
  }

  url_base = f"https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?"

  url_params = "&".join(
      [f'{key}={value}' for key, value in params.items()])
  final_url = f'{url_base}&{url_params}'

  response = requests.get(final_url)

  if response.status_code == 200:
    return response.json()
  else:
    raise HTTPException(status_code=response.status_code,
                        detail=response.reason)


class WeatherService(BaseService):
  def get_day_weather(self, location_id: int, since: str, to: str) -> WeatherSchema:
    """Get day weather."""

    since_datetime = datetime.strptime(since, '%Y-%m-%dT%H:%M:%S.%f%z')
    to_datetime = datetime.strptime(to, '%Y-%m-%dT%H:%M:%S.%f%z')

    weather_records = (
        self.session.query(Weather)
        .filter(Weather.location_id == location_id)
        .filter(and_(Weather.date >= since_datetime, Weather.date <= to_datetime))
        .order_by(Weather.date)
        .all()
    )

    weather_schema_list = [WeatherSchema.from_orm(
        weather) for weather in weather_records]

    return weather_schema_list

  def get_pvgis_data(self, params):
    return fetch_pvgis_data(**params)

  def test(self):
    data = calcular_parametros_solares(
        2022, 1, 1, 12, 0, -79.0286, -8.11167, 33, 15, 180)
    data_converted = {key: value.tolist() if isinstance(
        value, np.ndarray) else value for key, value in data.items()}

    data = json.dumps(data_converted, indent=2)

    return data_converted
