from fastapi import FastAPI
from version import __version__
from const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from routers import locations, weather, projects, users
from backend.database import engine
import models
from fastapi.middleware.cors import CORSMiddleware

models.SQLModel.metadata.create_all(bind=engine)

app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locations.router)
app.include_router(weather.router)
app.include_router(projects.router)
app.include_router(users.router)
