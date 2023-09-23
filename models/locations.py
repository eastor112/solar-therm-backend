from sqlalchemy import DateTime, Column, String, Boolean, Integer, Float, func
from models.base import SQLModel
from sqlalchemy.orm import relationship


class Location(SQLModel):
  __tablename__ = 'locations'
  id = Column(Integer, primary_key=True)
  place = Column(String, nullable=False)
  country = Column(String, nullable=False, server_default='Peru')
  lat = Column(Float, nullable=False)
  lng = Column(Float, nullable=False)
  altitude = Column(Float, nullable=False)
  is_calculated = Column(Boolean, nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  #
  weathers = relationship("Weather", back_populates="location")
  projects = relationship("Project", back_populates="location")
