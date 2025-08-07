from typing import Any

from src.bases_de_datos_en_notion.programas_en_notion import ProgramasEnNotion
from src.bases_de_datos_en_notion.nomina_en_notion import NominaEnNotion
from src.paginas_en_notion.bloque import BloqueDeContenido
from src.paginas_en_notion.profesor import Profesor
from src.documentos_en_word.programa import Programa


class Materia:
    _id: str
    _nombre: str
    _anio: str
    _carga_horaria: int
    _profesores_a_cargo: set[Profesor] = set()
    _contenido: list[BloqueDeContenido] = []

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
        return self

    async def descargar_contenido_asociado(self, programas: ProgramasEnNotion):
        self._contenido = await programas.consultar_programa_por_materia_id(self._id)
        return self

    def crear_documento_para_el_programa(self):
        documento = Programa(
            asignatura=self._nombre,
            anio_ciclo=self._anio,
            carga_horaria=self._carga_horaria,
        )

        documento.agregar_nombres_de_docentes(
            [str(profesor) for profesor in self._profesores_a_cargo]
        )

        documento.separar_tabla_con_datos_del_contenido()

        for bloque in self._contenido:
            bloque.insertar_en_documento(documento)

        return documento


class MateriaVacia(Materia):
    def __init__(self):
        self._id = ""
        self._anio = ""
        self._nombre = ""
        self._carga_horaria = 0
