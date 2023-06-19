import uuid
from .backend.database import Base, engine
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, text
from sqlalchemy.dialects.postgresql import UUID


class Location(Base):
  __tablename__ = 'locations'
  id = Column(Integer, primary_key=True)
  place = Column(String, nullable=False)
  country = Column(String, nullable=False, server_default='Peru')
  lat = Column(String, nullable=False)
  lng = Column(String, nullable=False)
  primary = Column(Boolean, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("now()"))
  updated_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("now()"))


class User(Base):
  __tablename__ = 'users'
  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
              default=uuid.uuid4)
  name = Column(String,  nullable=False)
  email = Column(String, unique=True, nullable=False)
  password = Column(String, nullable=False)
  photo = Column(String, nullable=True)
  role = Column(String, server_default='user', nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("now()"))
  updated_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("now()"))


Base.metadata.create_all(engine)
