from typing import Any
from pydantic import BaseModel, model_validator


class Profesor(BaseModel):
    nombre: str
    apellido: str

    @model_validator(mode="before")
    @classmethod
    def _parsear_propiedades_de_la_pagina(cls, data: Any) -> Any:
        propiedades = data["properties"]
        return {
            "nombre": propiedades["Nombre"]["rollup"]["array"][0]["formula"]["string"],
            "apellido": propiedades["Apellido"]["rollup"]["array"][0]["formula"][
                "string"
            ],
        }
