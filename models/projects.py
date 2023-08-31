from sqlalchemy import DateTime, Column, String, Boolean, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import SQLModel
from sqlalchemy.sql import func


class Project(SQLModel):
  __tablename__ = 'projects'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  pipeline_number = Column(Integer, nullable=True, default=0)
  pipeline_type = Column(Integer, nullable=True, default=0)
  volumen = Column(Float(), nullable=True, default=0.0)
  manifold = Column(Float(), nullable=True, default=0.0)
  date = Column(Date, nullable=True)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  deleted = Column(Boolean, default=False)
  location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  #
  user = relationship("User", back_populates="projects")
  location = relationship("Location", back_populates="projects")
