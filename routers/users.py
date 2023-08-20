from sqlalchemy.orm import Session
from backend.database import get_session
from schemas.projects import ProjectUpdateSchema
from schemas.users import UserCreateSchema, UserTokenValidationSchema
from services.users import UserService
from fastapi import (
    APIRouter,
    Depends,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post("/login")
async def login(payload: UserCreateSchema, session: Session = Depends(get_session)):
  return UserService(session).login(payload)


@router.post("/refresh")
async def get_user_by_token(payload: UserTokenValidationSchema, session: Session = Depends(get_session)):
  return UserService(session).get_user_by_token(payload)


@router.post("")
async def create_user(payload: UserCreateSchema, session: Session = Depends(get_session)):
  return UserService(session).create_user(payload)
