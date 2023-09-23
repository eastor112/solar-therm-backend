from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from schemas.users import UserRetrieveSchema


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
  pipeline_separation: Optional[float]
  inclination_deg: Optional[float]
  azimuth_deg: Optional[float]
  granularity: Optional[int]
  volumen: Optional[float]
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
  altitude: float
  is_calculated: bool

  class Config:
    orm_mode = True


class ProjectRetrieveSchema(ProjectSchema):

  pipeline_number: int | None
  pipeline_separation: float | None
  inclination_deg: float | None
  azimuth_deg: float | None
  granularity: int | None
  volumen: float | None
  manifold: float | None
  date: date | None
  location: LocationSchema | None
  user: UserRetrieveSchema

  class Config:
    orm_mode = True


class ProjectListResponseSchema(BaseModel):
  page: int
  total: int
  projects: List[ProjectRetrieveSchema]
  page_size: int
