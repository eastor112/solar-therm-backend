from dataclasses import Field
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class ProjectInitializeSchema(BaseModel):
  name: str
  user_id: int


class ProjectSchema(ProjectInitializeSchema):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True


class ProjectUpdateSchema(BaseModel):
  name: Optional[str]
  user_id: Optional[int]
  pipeline_number: Optional[int]
  pipeline_type: Optional[str]
  volumen: Optional[int]
  manifold: Optional[float]
  date: Optional[date]
  deleted: Optional[bool] = False
  location_id: Optional[int]


class LocationSchema(BaseModel):
  id: int
  place: str
  country: str
  lat: float
  lng: float
  is_calculated: bool

  class Config:
    orm_mode = True


class ProjectRetrieveSchema(BaseModel):
  id: int
  name: str
  user_id: int
  pipeline_number: int | None
  pipeline_type: str | None
  volumen: int | None
  manifold: float | None
  date: date | None
  deleted: bool | None
  location: LocationSchema | None

  class Config:
    orm_mode = True
