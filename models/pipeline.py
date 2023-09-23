from sqlalchemy import Column, String, Integer, Float
from models.base import SQLModel


class Pipeline(SQLModel):
  __tablename__ = 'pipelines'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  external_diameter = Column(Float(), nullable=True, default=0.0)
  internal_diameter = Column(Float(), nullable=True, default=0.0)
  long = Column(Float(), nullable=True, default=0.0)
