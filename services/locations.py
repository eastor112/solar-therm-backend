from typing import List

from sqlalchemy import text
from models.locations import Location
from schemas.locations import LocationResponseSchema, LocationCreateSchema
from services.base import (
    BaseService,
)


class LocationsService(BaseService):
  def get_locations(self) -> List[LocationCreateSchema]:
    """Get all locations."""

    locations = self.session.query(Location).all()
    return [LocationResponseSchema(**location.to_dict()) for location in locations]

  def get_location(self, location_id: int) -> LocationResponseSchema:
    """Get location by ID."""

    location = self.session.query(Location).get(location_id)

    if location:
      return LocationResponseSchema(**location.to_dict())
    return None

  def create_location(self, location: LocationCreateSchema) -> LocationResponseSchema:
    """Create location."""

    new_location = Location(**location.dict())
    self.session.add(new_location)
    self.session.commit()

    return LocationResponseSchema(**new_location.to_dict())
