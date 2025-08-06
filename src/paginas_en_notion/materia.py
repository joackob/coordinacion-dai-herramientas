from typing import Any

from src.bases_de_datos_en_notion.programas_en_notion import ProgramasEnNotion
from src.bases_de_datos_en_notion.nomina_en_notion import NominaEnNotion
from src.paginas_en_notion.bloque import BloqueDeContenido
from src.paginas_en_notion.profesor import Profesor


class Materia:
    _id: str
    _nombre: str
    _anio: str
    _carga_horaria: int
    _profesores_a_cargo: set[Profesor] = set()
    _programa: list[BloqueDeContenido] = []

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

    async def descargar_programa(self, materias: ProgramasEnNotion):
        self._programa = await materias.consultar_por_programa_de_una_materia_por_su_id(
            self._id
        )


class MateriaVacia(Materia):
    def __init__(self):
        self._id = ""
        self._anio = ""
        self._nombre = ""
        self._carga_horaria = 0
