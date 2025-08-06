from typing import Any
from pydantic import BaseModel, model_validator


class Profesor(BaseModel):
    _nombre: str
    _apellido: str

    def __init__(self, data: Any):
        propiedades = data["properties"]
        self._nombre = propiedades["Nombre"]["rollup"]["array"][0]["formula"]["string"]
        self._apellido = propiedades["Apellido"]["rollup"]["array"][0]["formula"][
            "string"
        ]
