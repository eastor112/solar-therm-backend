from pydantic import BaseModel


class LocationSchema(BaseModel):
  place: str
  country:  str
  lat: float
  lng: float
  primary: bool
