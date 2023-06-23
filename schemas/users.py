from pydantic import BaseModel


class UserLoginSchema(BaseModel):
  email: str
  password: str


class UserTokenValidationSchema(BaseModel):
  token: str


class UserCreateSchema(BaseModel):
  email: str
  password: str
  first_name: str | None
  last_name: str | None


class UserSchema(UserLoginSchema):
  id: int
  email: str
  password: str
  first_name: str | None
  last_name: str | None
  token: str
  is_admin: bool

  class Config:
    orm_mode = True
