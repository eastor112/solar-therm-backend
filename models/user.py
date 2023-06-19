from sqlalchemy import Column, String, Boolean, Integer, text
from sqlalchemy.orm import relationship
from models.base import SQLModel


class User(SQLModel):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  email = Column(String(60), nullable=False, unique=True)
  password = Column(String(50), nullable=False)
  first_name = Column(String(50), nullable=False)
  last_name = Column(String(50), nullable=False)
  is_admin = Column(Boolean, default=False)
  projects = relationship("Project", back_populates="user")
