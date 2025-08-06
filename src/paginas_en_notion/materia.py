from typing import Any

from src.bases_de_datos_en_notion.nomina_en_notion import NominaEnNotion
from src.paginas_en_notion.profesor import Profesor


class Materia:
    _id: str
    _nombre: str
    _anio: str
    _carga_horaria: int
    _profesores_a_cargo: set[Profesor] = set()

    def __init__(self, data: Any):
        propiedades = data["results"][0]["properties"]
        self._id = data["results"][0]["id"]
        self._nombre = propiedades["Nombre"]["formula"]["string"]
        self._anio = propiedades["Año"]["select"]["name"]
        self._carga_horaria = propiedades["Carga Horaria Semanal"]["number"]

    async def determinar_profesores_a_cargo(self, nomina: NominaEnNotion):
        self._profesores_a_cargo = await nomina.consultar_por_profesores_de_una_materia(
            self._nombre
        )

    @property
    def anio(self) -> str:
        return self._anio

    @property
    def nombre(self) -> str:
        return self._nombre


class MateriaVacia(Materia):
    def __init__(self):
        self._id = ""
        self._anio = ""
        self._nombre = ""
        self._carga_horaria = 0
