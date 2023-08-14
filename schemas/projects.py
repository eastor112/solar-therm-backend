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
  pipeline_type: Optional[int]
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
  is_calculated: bool

  class Config:
    orm_mode = True


class ProjectRetrieveSchema(BaseModel):
  id: int
  name: str
  user_id: int
  pipeline_number: int | None
  pipeline_type: int | None
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
