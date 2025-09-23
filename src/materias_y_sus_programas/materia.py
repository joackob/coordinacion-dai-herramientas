from typing import Any

from src.bases_de_datos_en_notion.programas import Programas
from src.bases_de_datos_en_notion.nomina import Nomina
from src.materias_y_sus_programas.bloque import BloqueDeContenido
from src.materias_y_sus_programas.profesor import Profesor
from src.documentos_en_word.programa import Programa


class Materia:

    def __init__(self, data: Any):
        propiedades = data["properties"]
        self._id = data["id"]
        self._nombre = propiedades["Nombre"]["formula"]["string"]
        self._area = propiedades["Área"]["select"]["name"]
        self._anio = propiedades["Año"]["select"]["name"]
        self._carga_horaria = propiedades["Carga Horaria Semanal"]["number"]
        self._profesores_a_cargo: set[Profesor] = set()
        self._contenido: list[BloqueDeContenido] = []

    async def determinar_profesores_a_cargo(self, nomina: Nomina):
        self._profesores_a_cargo = await nomina.consultar_por_profesores_de_una_materia(
            self._nombre
        )
        return self

    async def descargar_contenido_asociado(self, programas: Programas):
        self._contenido = await programas.consultar_programa_por_materia_id(self._id)
        return self

    def crear_documento_para_el_programa(self) -> Programa:
        documento = Programa(
            asignatura=self._nombre,
            anio=self._anio,
            carga_horaria=self._carga_horaria,
            area=self._area,
        )

        documento.agregar_nombres_de_docentes(
            [str(profesor) for profesor in self._profesores_a_cargo]
        )

        documento.separar_tabla_con_datos_del_contenido()

        for bloque in self._contenido:
            bloque.insertar_en_documento(documento)

        return documento
