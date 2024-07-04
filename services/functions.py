import pytz
import requests
from functools import lru_cache
from fastapi import HTTPException
from datetime import datetime


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
