from fastapi import FastAPI
from version import __version__
from const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from routers import locations
from backend.database import engine
import models

models.SQLModel.metadata.create_all(bind=engine)


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


app.include_router(locations.router)
