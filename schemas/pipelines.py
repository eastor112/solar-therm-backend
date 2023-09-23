from pydantic import BaseModel
from typing import Optional


class PipelineCreateSchema(BaseModel):
  name: str
  external_diameter: Optional[float] = 0.0
  internal_diameter: Optional[float] = 0.0
  length: Optional[float] = 0.0


class PipelineUpdateSchema(BaseModel):
  name: Optional[str]
  external_diameter: Optional[float]
  internal_diameter: Optional[float]
  length: Optional[float]


class PipelineRetrieveSchema(BaseModel):
  id: int
  name: str
  external_diameter: float
  internal_diameter: float
  length: float
