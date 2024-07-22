from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from schemas.pipelines import PipelineRetrieveSchema
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
  pipeline: PipelineRetrieveSchema | None

  @classmethod
  def from_orm(cls, project):
    model = super().from_orm(project)

    # Formatear la fecha de YYYY-MM-DD a DD-MM-YYYY
    if model.date:
      model.date = datetime.strftime(model.date, "%d-%m-%Y")

    return model

  class Config:
    orm_mode = True


class ProjectListResponseSchema(BaseModel):
  page: int
  total: int
  projects: List[ProjectRetrieveSchema]
  page_size: int


class NewProjectInitializeSchema(BaseModel):
  name_project: str
  place: int
  latitud: float
  longitud: float
  t_amb: float
  v_viento: float
  altitud: float
  date_time: datetime
  inclinacion: float
  azimuth: float
  vol_tank: float
  e_tank: float
  e_aisl: float
  e_cub: float
  h_int: float
  h_ext: float
  k_tank: float
  k_aisl: float
  k_cub: float
  d_int: float
  d_ext: float
  longitud_tubo: float
  s_sep: float
  num_tubos: int
  tau_glass: float
  alfa_glass: float
  n_div: int
  nn: int
  beta_coef: float
  f_flujo: float
  user_id: int


class NewProjectSchema(NewProjectInitializeSchema):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True


class NewProjectUpdateSchema(BaseModel):
  name_project: Optional[str]
  place: Optional[int]
  latitud: Optional[float]
  longitud: Optional[float]
  t_amb: Optional[float]
  v_viento: Optional[float]
  altitud: Optional[float]
  date_time: Optional[datetime]
  inclinacion: Optional[float]
  azimuth: Optional[float]
  vol_tank: Optional[float]
  e_tank: Optional[float]
  e_aisl: Optional[float]
  e_cub: Optional[float]
  h_int: Optional[float]
  h_ext: Optional[float]
  k_tank: Optional[float]
  k_aisl: Optional[float]
  k_cub: Optional[float]
  d_int: Optional[float]
  d_ext: Optional[float]
  longitud_tubo: Optional[float]
  s_sep: Optional[float]
  num_tubos: Optional[int]
  tau_glass: Optional[float]
  alfa_glass: Optional[float]
  n_div: Optional[int]
  nn: Optional[int]
  beta_coef: Optional[float]
  f_flujo: Optional[float]
  user_id: Optional[int]


class NewProjectRetrieveSchema(NewProjectSchema):
  user: UserRetrieveSchema

  class Config:
    orm_mode = True
    from_attributes = True
    json_encoders = {
        datetime: lambda v: v.isoformat()
    }


class NewProjectListResponseSchema(BaseModel):
  page: int
  total: int
  projects: List[NewProjectRetrieveSchema]
  page_size: int
