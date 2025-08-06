from typing import Any
from pydantic import BaseModel, model_validator


class Materia(BaseModel):
    id: str
    nombre: str
    anio: str
    carga_horaria: int

    @model_validator(mode="before")
    @classmethod
    def _parsear_propiedades_de_la_pagina(cls, data: Any) -> Any:
        propiedades = data["results"][0]["properties"]
        return {
            "nombre": propiedades["Nombre"]["formula"]["string"],
            "anio": propiedades["Año"]["select"]["name"],
            "carga_horaria": propiedades["Carga Horaria Semanal"]["number"],
            "id": data["results"][0]["id"],
        }


class MateriaVacia(Materia):
    def __init__(self):
        pass

    pass
