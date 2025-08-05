from typing import Any
from pydantic import BaseModel, model_validator
from src.Materia import Materia, MateriaVacia


class PaginaDeNotion(BaseModel):
    nombre: str
    anio: str
    carga_horaria: int
    # docentes: list[str]

    def exportar_a_materia(self) -> Materia:
        return Materia(
            nombre=self.nombre,
            anio=self.anio,
            carga_horaria=self.carga_horaria,
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
            "carga_horaria": propiedades["Carga Horaria Semanal"]["number"],
        }

    # @model_validator(mode="after")
    # def _validar_docentes(self):
    #     if len(self.docentes) == 0:
    #         raise ValueError("La lista de docentes no puede estar vacía")
    #     return self


class PaginaDeNotionVacia(PaginaDeNotion):
    def __init__(self):
        pass

    def exportar_a_materia(self) -> Materia:
        return MateriaVacia()

    pass
