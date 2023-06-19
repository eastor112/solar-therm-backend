from sqlalchemy import ForeignKey, Column, DateTime, Float, Integer, ForeignKey
from models.base import SQLModel
from sqlalchemy.orm import relationship


class Weather(SQLModel):
  __tablename__ = 'weather'

  id = Column(Integer, primary_key=True)
  dhi = Column(Integer)
  temperature = Column(Float)
  clearsky_dhi = Column(Integer)
  clearsky_dni = Column(Integer)
  clearsky_ghi = Column(Integer)
  dni = Column(Integer)
  ghi = Column(Integer)
  cloud_type = Column(Integer)
  relative_humidity = Column(Float)
  solar_zenith_angle = Column(Float)
  wind_direction = Column(Integer)
  wind_speed = Column(Float)
  location_id = Column(Integer, ForeignKey('locations.id'))
  date = Column(DateTime(timezone=True))
  #
  location = relationship("Location", back_populates="weathers")
