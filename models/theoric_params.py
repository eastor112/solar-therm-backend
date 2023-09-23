from sqlalchemy import Column, ForeignKey, Integer, Float
from models.base import SQLModel


class TheoricParams(SQLModel):
  __tablename__ = 'theoric_params'
  id = Column(Integer, primary_key=True, autoincrement=True)
  inclination_deg = Column(Float(), default=0.0)
  azimuth_deg = Column(Float(), default=0.0)
  granularity = Column(Integer, default=24)
  location_id = Column(Integer, ForeignKey("locations.id"))
  pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
