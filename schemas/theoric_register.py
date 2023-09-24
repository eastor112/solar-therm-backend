from pydantic import BaseModel
from typing import Optional


class TheoricRegisterCreateSchema(BaseModel):
  day: int
  energy: Optional[float] = 0.0
  params_id: int


class TheoricRegisterUpdateSchema(BaseModel):
  day: Optional[int]
  energy: Optional[float]
  params_id: Optional[int]


class TheoricRegisterRetrieveSchema(BaseModel):
  id: int
  day: int
  energy: float
  params_id: int
