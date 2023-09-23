from sqlalchemy import Column, Float, ForeignKey, Integer
from models.base import SQLModel
from sqlalchemy.orm import relationship


class TheoricRegister(SQLModel):
  __tablename__ = 'theoric_register'
  id = Column(Integer, primary_key=True, autoincrement=True)
  day = Column(Integer)
  energy = Column(Float(), default=0.0)
  params_id = Column(Integer, ForeignKey("theoric_params.id"))
  #
  theoretic_params = relationship(
      "TheoricParams", back_populates="theoric_register")
