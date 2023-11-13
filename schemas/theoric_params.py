from pydantic import BaseModel
from typing import Optional, List
from schemas.projects import LocationSchema


class TheoricParamsCreateSchema(BaseModel):
  inclination_deg: float = 0.0
  azimuth_deg: float = 0.0
  granularity: int = 24
  pipeline_separation: Optional[float] = 0.0
  location_id: int
  pipeline_id: int
  project_id: int


class TheoricParamsUpdateSchema(BaseModel):
  inclination_deg: Optional[float]
  azimuth_deg: Optional[float]
  granularity: Optional[int]
  pipeline_separation: Optional[float]
  location_id: Optional[int]
  pipeline_id: Optional[int]


class TheoricParamsDeleteSchema(BaseModel):
  params_ids: List[int]


class PipelineRetrieveSchema(BaseModel):
  id: int
  name: str
  external_diameter: float
  internal_diameter: float
  length: float

  class Config:
    orm_mode = True


class TheoricParamsRetriveSchema(BaseModel):
  id: int
  inclination_deg: float
  azimuth_deg: float
  granularity: int
  pipeline_separation: float
  location: LocationSchema
  pipeline: PipelineRetrieveSchema
  project_id: int

  class Config:
    orm_mode = True


class EnergyCalculatorRequestSchema(BaseModel):
  local_longitude: float
  local_latitude: float
  local_height: float
  inclination: float
  azimuth: float
  internal_diameter: float
  external_diameter: float
  pipeline_length: float
  pipeline_separation: float
  granularity: int
