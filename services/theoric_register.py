from typing import List
from sqlalchemy.orm import Session
from schemas.theoric_register import TheoricRegisterCreateSchema, TheoricRegisterRetrieveSchema
from models.theoric_register import TheoricRegister
from models.theoric_params import TheoricParams


class TheoricRegisterService:
  def create_theoric_registers(self, session: Session, registers: List[TheoricRegisterCreateSchema]):
    created_registers = []
    for register in registers:
      db_register = TheoricRegister(**register.dict())
      session.add(db_register)
    session.commit()
    return [TheoricRegisterRetrieveSchema(**register.dict()) for register in created_registers]

  def get_registers_by_params_id(self, session: Session, params_id: int) -> List[TheoricRegisterRetrieveSchema]:
    registers = session.query(TheoricRegister).filter(
        TheoricRegister.params_id == params_id).all()
    return [TheoricRegisterRetrieveSchema(**register.to_dict()) for register in registers]

  def delete_registers_by_params_id(self, session: Session, params_id: int):
    deleted_count = session.query(TheoricRegister).filter(
        TheoricRegister.params_id == params_id).delete()
    session.commit()
    return deleted_count

  def get_registers_grouped_by_project(self, session, project_id: int) -> List[List[TheoricRegisterRetrieveSchema]]:
    params = session.query(TheoricParams.id.label('param_id')).filter(
        TheoricParams.project_id == project_id
    ).all()

    result = []

    for param in params:
      param_id = param.param_id

      registers = session.query(TheoricRegister).filter(
          TheoricRegister.params_id == param_id).all()

      register_list = [TheoricRegisterRetrieveSchema(
          **register.to_dict()) for register in registers]

      if (len(register_list) > 0):
        result.append(register_list)

    return result
