from enum import Enum
from typing import (
    Final,
    List,
)


# Open API parameters
OPEN_API_TITLE: Final = "SolarTherm"
OPEN_API_DESCRIPTION: Final = "API de consulta de datos climatológicos de Perú - Projecto diseño de termas solares de alta eficiencia"

# Authentication service constants
AUTH_TAGS: Final[List[str | Enum] | None] = ["Authentication"]
AUTH_URL: Final = "token"

TOKEN_TYPE: Final = "bearer"
TOKEN_EXPIRE_MINUTES: Final = 60

# Algorithm used to sign the JWT tokens
TOKEN_ALGORITHM: Final = "HS256"
