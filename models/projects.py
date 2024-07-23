from sqlalchemy.sql import func
from models.base import SQLModel
from sqlalchemy import (DateTime, Column, String, Boolean,
                        Integer, Float, Date, ForeignKey)
from sqlalchemy.orm import relationship


class Project(SQLModel):
  __tablename__ = 'projects'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  pipeline_number = Column(Integer, nullable=True, default=0)
  pipeline_separation = Column(Float(), nullable=True, default=0.0)
  inclination_deg = Column(Float(), nullable=True, default=0.0)
  azimuth_deg = Column(Float(), nullable=True, default=0.0)
  granularity = Column(Integer, nullable=True, default=0)
  volumen = Column(Float(), nullable=True, default=0.0)
  manifold = Column(Float(), nullable=True, default=0.0)
  date = Column(Date, nullable=True)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  deleted = Column(Boolean, default=False)
  pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
  location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  #
  user = relationship("User", back_populates="projects")
  location = relationship("Location", back_populates="projects")
  pipeline = relationship("Pipeline", back_populates="projects")
  theoric_params = relationship("TheoricParams", back_populates="project")


class NewProject(SQLModel):
  __tablename__ = 'new_projects'

  name_project = Column(String(50), nullable=False)
  id = Column(Integer, primary_key=True, autoincrement=True)
  place = Column(Integer, nullable=False)
  latitud = Column(Float, nullable=False)
  longitud = Column(Float, nullable=False)
  t_amb = Column(Float, nullable=False)
  v_viento = Column(Float, nullable=False)
  altitud = Column(Float, nullable=False)
  date_time = Column(DateTime, nullable=False)
  inclinacion = Column(Float, nullable=False)
  azimuth = Column(Float, nullable=False)
  vol_tank = Column(Float, nullable=False)
  e_tank = Column(Float, nullable=False)
  e_aisl = Column(Float, nullable=False)
  e_cub = Column(Float, nullable=False)
  h_int = Column(Float, nullable=False)
  h_ext = Column(Float, nullable=False)
  k_tank = Column(Float, nullable=False)
  k_aisl = Column(Float, nullable=False)
  k_cub = Column(Float, nullable=False)
  d_int = Column(Float, nullable=False)
  d_ext = Column(Float, nullable=False)
  longitud_tubo = Column(Float, nullable=False)
  s_sep = Column(Float, nullable=False)
  num_tubos = Column(Integer, nullable=False)
  tau_glass = Column(Float, nullable=False)
  alfa_glass = Column(Float, nullable=False)
  n_div = Column(Integer, nullable=False)
  nn = Column(Integer, nullable=False)
  beta_coef = Column(Float, nullable=False)
  f_flujo = Column(Float, nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  user_id = Column(Integer, ForeignKey("users.id"))
  #
  user = relationship("User", back_populates="new_projects")

  class Config:
    from_attributes = True
    json_schema_extra = {
        "example": {
            "name_project": "test",
            "place": 0,
            "latitud": -8.11599,
            "longitud": -79.02998,
            "t_amb": 25,
            "v_viento": 2.5,
            "altitud": 33,
            "date_time": "2018-12-27T12:00:00-05:00",
            "inclinacion": 15,
            "azimuth": 180,
            "vol_tank": 0.3,
            "e_tank": 0.0004,
            "e_aisl": 0.005,
            "e_cub": 0.0004,
            "h_int": 10,
            "h_ext": 25,
            "k_tank": 14.9,
            "k_aisl": 0.06,
            "k_cub": 14.9,
            "d_int": 0.048,
            "d_ext": 0.058,
            "longitud_tubo": 1.8,
            "s_sep": 0.056,
            "num_tubos": 30,
            "tau_glass": 0.93,
            "alfa_glass": 0.89,
            "n_div": 12,
            "nn": 360,
            "beta_coef": 0.000257,
            "f_flujo": 0.45,
            "user_id": 1
        }
    }
