from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean
from models.base import SQLModel
from sqlalchemy.orm import relationship


class TheoricParams(SQLModel):
  __tablename__ = 'theoric_params'
  id = Column(Integer, primary_key=True)
  inclination_deg = Column(Float(), default=0.0)
  azimuth_deg = Column(Float(), default=0.0)
  granularity = Column(Integer, default=24)
  pipeline_separation = Column(Float(), nullable=True, default=0.0)
  isCalculated = Column(Boolean, nullable=False)
  location_id = Column(Integer, ForeignKey("locations.id"))
  pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
  project_id = Column(Integer, ForeignKey("projects.id"))
  #
  pipeline = relationship("Pipeline", back_populates="theoric_params")
  location = relationship("Location", back_populates="theoric_params")
  theoric_register = relationship(
      "TheoricRegister", back_populates="theoric_params")
  project = relationship("Project", back_populates="theoric_params")
