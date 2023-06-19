from sqlalchemy import DateTime, Column, String, Boolean, Integer, Float, text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import SQLModel
from sqlalchemy.sql import func


class Project(SQLModel):
  __tablename__ = 'projects'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  pipeline_number = Column(Integer, nullable=False)
  pipeline_type = Column(String(50), nullable=False)
  volumen = Column(Integer, nullable=False)
  manifold = Column(Float(50), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  deleted = Column(Boolean, default=False)
  user_id = Column(Integer, ForeignKey("users.id"))
  #
  user = relationship("User", back_populates="projects")
