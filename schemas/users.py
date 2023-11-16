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


class UserRetrieveSchema(BaseModel):
  id: int
  email: str
  first_name: str | None
  last_name: str | None
  is_admin: bool

  class Config:
    orm_mode = True


class UserSchema(BaseModel):
  id: int
  email: str
  first_name: str | None
  last_name: str | None
  token: str
  is_admin: bool

  class Config:
    orm_mode = True
