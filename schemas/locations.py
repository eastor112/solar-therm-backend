from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LocationCreateSchema(BaseModel):
  place: str
  country:  str
  lat: float
  lng: float
  altitude: float
  is_calculated: bool = False


class LocationResponseSchema(BaseModel):
  id: int
  place: str
  country: str
  lat: float
  lng: float
  altitude: float
  is_calculated: bool
  created_at: datetime = Field(..., alias='created_at')
  updated_at: datetime = Field(..., alias='updated_at')

  class Config:
    orm_mode = True


class LocationUpdateSchema(BaseModel):
  place: Optional[str]
  country: Optional[str]
  lat: Optional[float]
  lng: Optional[float]
  altitude: Optional[float]
  is_calculated: Optional[bool]
