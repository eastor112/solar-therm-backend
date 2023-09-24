from typing import List
from models.locations import Location
from models.pipeline import Pipeline
from models.theoric_register import TheoricRegister
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

  def calculate_annual_energy_from_params(self, theoric_param_id: int) -> bool:
    current_theoric_params = self.session.query(TheoricParams) \
        .filter(TheoricParams.id == theoric_param_id) \
        .join(TheoricParams.location) \
        .join(TheoricParams.pipeline) \
        .first()

    params = {
        "local_longitude": current_theoric_params.location.lng,
        "local_latitude": current_theoric_params.location.lat,
        "local_height": current_theoric_params.location.altitude,
        "inclination": current_theoric_params.inclination_deg,
        "azimuth": current_theoric_params.azimuth_deg,
        "internal_diameter": current_theoric_params.pipeline.internal_diameter,
        "external_diameter": current_theoric_params.pipeline.external_diameter,
        "pipeline_length": current_theoric_params.pipeline.length,
        "pipeline_separation": current_theoric_params.pipeline_separation,
        "granularity": current_theoric_params.granularity,
    }

    duplicate_params = self.session.query(TheoricParams).filter(
        TheoricParams.isCalculated == True,
        TheoricParams.azimuth_deg == params['azimuth'],
        TheoricParams.inclination_deg == params['inclination'],
        TheoricParams.granularity == params['granularity'],
        TheoricParams.pipeline_separation == params['pipeline_separation'],
    ).join(TheoricParams.location).join(TheoricParams.pipeline).filter(
        Location.lng == params['local_longitude'],
        Location.lat == params['local_latitude'],
        Location.altitude == params['local_height'],
        Pipeline.internal_diameter == params['internal_diameter'],
        Pipeline.external_diameter == params['external_diameter'],
        Pipeline.length == params['pipeline_length'],
    ).first()

    if not duplicate_params:
      _, daily_energy = calculate_annual_energy(**params)

      for day, energy in enumerate(daily_energy, start=1):
        theoric_register = TheoricRegister(
            day=day,
            energy=energy,
            params_id=theoric_param_id
        )
        self.session.add(theoric_register)

      current_theoric_params.isCalculated = True
      self.session.commit()
      return {"message": "Calculation successful"}

    return {"message": "Calculation successful (duplicated)"}
