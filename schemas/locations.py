from pydantic import BaseModel, Field
from datetime import datetime


class LocationCreateSchema(BaseModel):
  place: str
  country:  str
  lat: float
  lng: float
  is_calculated: bool = False


class LocationResponseSchema(BaseModel):
  id: int
  place: str
  country: str
  lat: float
  lng: float
  is_calculated: bool
  created_at: datetime = Field(..., alias='created_at')
  updated_at: datetime = Field(..., alias='updated_at')

  class Config:
    orm_mode = True
