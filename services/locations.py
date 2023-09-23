from typing import List

from models.locations import Location
from schemas.locations import LocationResponseSchema, LocationCreateSchema, LocationUpdateSchema
from services.base import BaseService


class LocationsService(BaseService):
  def get_locations(self) -> List[LocationResponseSchema]:
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

  def update_location(self, location_id: int, location_data: LocationUpdateSchema) -> LocationResponseSchema:
    """Update location by ID."""
    location = self.session.query(Location).get(location_id)
    if location:
      for attr, value in location_data.dict(exclude_unset=True, exclude_defaults=True).items():
        setattr(location, attr, value)
      self.session.commit()
      return LocationResponseSchema(**location.to_dict())
    return None

  def delete_location(self, location_id: int) -> bool:
    """Delete location by ID."""
    location = self.session.query(Location).get(location_id)
    if location:
      self.session.delete(location)
      self.session.commit()
      return True
    return False
