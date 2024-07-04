from datetime import datetime
from sqlalchemy import and_
from models.weather import Weather
from schemas.weather import WeatherSchema
from thermal_model.results import get_therma_results
import json
import numpy as np
import pytz
import requests
from functools import lru_cache
from fastapi import HTTPException
from datetime import datetime


from services.base import (
    BaseService,
)


@lru_cache(maxsize=128)
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
    data = response.json()
    lima_tz = pytz.timezone('America/Lima')

    for entry in data['outputs']['hourly']:
      dt_naive = datetime.strptime(entry['time'], '%Y%m%d:%H%M')
      dt_utc = pytz.utc.localize(dt_naive)
      dt_lima = dt_utc.astimezone(lima_tz)
      entry['time'] = dt_lima.strftime('%Y-%m-%dT%H:%M:%S%z')
    return data
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
    date_time = "2020-01-01T12:00:00-05:00"

    thermal_data = fetch_pvgis_data(
        -8.11167,
        -79.0286,
        "PVGIS-ERA5",
        2020,
        2020,
        15,
        180,
        "json"
    )

    params = {
        'thermal_data':  thermal_data['outputs']['hourly'],
        'date_time': date_time,
        'latitud_local': -8.11167,
        'longitud_local': -79.0286,
        'altitud_local': 33,
        'inclinacion': 15,
        'azimuth': 180,
        't_amb': 20,
        'v_viento': 3,
        'd_int': 0.048,
        'd_ext': 0.058,
        'lon_tubo': 1.8,
        's_sep': 0.056,
        'vol_tank': 0.3,
        'num_tubos': 30,
        'e_tank': 0.0004,
        'e_aisl': 0.005,
        'e_cub': 0.0004,
        'tau_glass': 0.93,
        'alfa_glass': 0.89,
        'h_int': 10,
        'h_ext': 15,
        'k_tank': 14.9,
        'k_aisl': 0.06,
        'k_cub': 14.9,
        'f_flujo': 0.45,
        'beta_coef': 0.000257,
        'nn': 361,
        'n_div': 12,
    }

    results = get_therma_results(params)
    data_converted = {key: value.tolist() if isinstance(
        value, np.ndarray) else value for key, value in results.items()}

    results = json.dumps(data_converted, indent=2)

    return data_converted
