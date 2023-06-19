from typing import List

from sqlalchemy import text
from models.locations import Location
from schemas.locations import LocationSchema
from services.base import (
    BaseService,
)


class LocationsService(BaseService):
  def get_locations(self) -> List[LocationSchema]:
    """Get all locations."""

    locations = self.session.query(Location).all()
    return [LocationSchema(**location.to_dict()) for location in locations]

  def get_location(self, location_id: int) -> LocationSchema:
    """Get location by ID."""

    location = self.session.query(Location).get(location_id)

    if location:
      return LocationSchema(**location.to_dict())
    return None
