from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, text
from models.base import SQLModel
from sqlalchemy.orm import relationship


class Location(SQLModel):
  __tablename__ = 'locations'
  id = Column(Integer, primary_key=True)
  place = Column(String, nullable=False)
  country = Column(String, nullable=False, server_default='Peru')
  lat = Column(String, nullable=False)
  lng = Column(String, nullable=False)
  primary = Column(Boolean, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("now()"))
  updated_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("now()"))
  weathers = relationship("Weather", back_populates="location")
