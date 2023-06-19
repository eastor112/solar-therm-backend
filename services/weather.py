from datetime import datetime
from sqlalchemy import and_
from models.weather import Weather
from schemas.weather import WeatherSchema

from services.base import (
    BaseService,
)


class WeatherService(BaseService):
  def get_day_weather(self, location_id: int, since: str, to: str) -> WeatherSchema:
    """Get day weather."""
    since_datetime = datetime.strptime(since, "%Y-%m-%dT%H:%M:%S.%fZ")
    to_datetime = datetime.strptime(to, "%Y-%m-%dT%H:%M:%S.%fZ")

    weather_records = (
        self.session.query(Weather)
        .filter(Weather.location_id == location_id)
        .filter(and_(Weather.date >= since_datetime, Weather.date <= to_datetime))
        .all()
    )

    weather_schema_list = [WeatherSchema.from_orm(
        weather) for weather in weather_records]

    return weather_schema_list
