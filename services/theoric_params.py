from typing import List
from schemas.theoric_params import (
    EnergyCalculatorRequestSchema,
    TheoricParamsCreateSchema,
    TheoricParamsUpdateSchema,
    TheoricParamsRetriveSchema,
)
from models.theoric_params import TheoricParams
from services.base import BaseService
from thermal_model.pipeline_energy_anual import calculate_annual_energy


class TheoricParamsService(BaseService):
  def get_all_theoric_params(self) -> List[TheoricParamsRetriveSchema]:
    """Get all theoric_params."""
    theoric_params = self.session.query(TheoricParams).all()
    return [TheoricParamsRetriveSchema.from_orm(theoric_param) for theoric_param in theoric_params]

  def get_theoric_param(self, theoric_param_id: int) -> TheoricParamsRetriveSchema:
    """Get theoric_param by ID."""

    theoric_param = self.session.query(TheoricParams).get(theoric_param_id)
    if theoric_param:
      return TheoricParamsRetriveSchema.from_orm(theoric_param)
    return None

  def create_theoric_param(self, theoric_param: TheoricParamsCreateSchema) -> TheoricParamsRetriveSchema:
    """Create theoric_param."""
    new_theoric_param = TheoricParams(**theoric_param.dict())
    self.session.add(new_theoric_param)
    self.session.commit()
    return TheoricParamsRetriveSchema.from_orm(new_theoric_param)

  def update_theoric_param(
      self, theoric_param_id: int, theoric_param: TheoricParamsUpdateSchema
  ) -> TheoricParamsRetriveSchema:
    """Update theoric_param by ID."""
    theoric_param_to_update = self.session.query(
        TheoricParams).get(theoric_param_id)
    if theoric_param_to_update:
      for attr, value in theoric_param.dict(exclude_unset=True, exclude_defaults=True).items():
        setattr(theoric_param_to_update, attr, value)
      self.session.commit()
      return TheoricParamsRetriveSchema.from_orm(theoric_param_to_update)
    return None

  def delete_theoric_param(self, theoric_param_id: int) -> bool:
    """Delete theoric_param by ID."""
    theoric_param_to_delete = self.session.query(
        TheoricParams).get(theoric_param_id)
    if theoric_param_to_delete:
      self.session.delete(theoric_param_to_delete)
      self.session.commit()
      return True
    return False

  def calculate_annual_energy(self, request_data: EnergyCalculatorRequestSchema) -> dict:
    """Calculate the annual energy captured by a solar collector."""
    calculation_data = request_data.dict()

    annual_energy, daily_energy = calculate_annual_energy(**calculation_data)

    return {"message": "Calculation successful", "total": annual_energy}
