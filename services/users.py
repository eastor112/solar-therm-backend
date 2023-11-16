from models import User
from schemas.users import UserCreateSchema, UserLoginSchema, UserSchema, UserTokenValidationSchema
from services.base import BaseService
import secrets
import string
from fastapi import HTTPException, status


class UserService(BaseService):
  def login(self, payload: UserLoginSchema) -> UserSchema:
    """Login user."""

    user = self.session.query(User).filter(User.email == payload.email).first()

    if user and user.password == (payload.password):
      return UserSchema(**user.to_dict())
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  def get_user_by_token(self, payload: UserTokenValidationSchema) -> UserSchema:
    """Get user by token."""
    user = self.session.query(User).filter(User.token == payload.token).first()

    if user:
      return UserSchema(**user.to_dict())
    raise HTTPException(status_code=404, detail="User not found")

  def create_user(self, payload: UserCreateSchema) -> UserSchema:
    """Create user."""

    user = User(**payload.dict(), token=''.join(secrets.choice(string.ascii_letters +
                string.digits + string.punctuation) for _ in range(35)))
    self.session.add(user)
    self.session.commit()
    return UserSchema(**user.to_dict())
