from sqlalchemy import Column, ForeignKey, Integer, Float
from models.base import SQLModel
from sqlalchemy.orm import relationship


class TheoricParams(SQLModel):
  __tablename__ = 'theoric_params'
  id = Column(Integer, primary_key=True, autoincrement=True)
  inclination_deg = Column(Float(), default=0.0)
  azimuth_deg = Column(Float(), default=0.0)
  granularity = Column(Integer, default=24)
  pipeline_separation = Column(Float(), nullable=True, default=0.0)
  location_id = Column(Integer, ForeignKey("locations.id"))
  pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
  #
  location = relationship("Location", back_populates="theoric_params")
  pipeline = relationship("Pipeline", back_populates="theoric_params")
