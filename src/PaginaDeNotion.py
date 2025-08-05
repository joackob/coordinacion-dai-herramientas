from typing import Any
from pydantic import BaseModel, model_validator
from src.Materia import Materia, MateriaVacia


class PaginaDeNotion(BaseModel):
    nombre: str
    anio: str
    carga_horaria: int

    def exportar_a_materia(self) -> Materia:
        return Materia(
            nombre=self.nombre,
            anio=self.anio,
            carga_horaria=8,
            jefx_de_departamento="jefx de departamento",
            docentes=["docente1", "docente2"],
            contenido=["contenido1", "contenido2"],
        )

    @model_validator(mode="before")
    @classmethod
    def _parsear_propiedades_de_la_pagina(cls, data: Any) -> Any:
        propiedades = data["results"][0]["properties"]
        return {
            "nombre": propiedades["Nombre"]["formula"]["string"],
            "anio": propiedades["Año"]["select"]["name"],
            "carga_horaria": propiedades["Carga horaria semanal"]["number"],
        }


class PaginaDeNotionVacia(PaginaDeNotion):
    def __init__(self):
        pass

    def exportar_a_materia(self) -> Materia:
        return MateriaVacia()

    pass
