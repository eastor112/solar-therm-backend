from sqlalchemy import Column, Float, ForeignKey, Integer
from models.base import SQLModel


class TheoricRegister(SQLModel):
  __tablename__ = 'theoric_register'
  id = Column(Integer, primary_key=True, autoincrement=True)
  day = Column(Integer)
  energy = Column(Float(), default=0.0)
  params_id = Column(Integer, ForeignKey("theoric_params.id"))
