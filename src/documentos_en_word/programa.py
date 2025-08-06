from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table
from pathlib import Path

# ubicacion_logo_de_cabecera = "src/documentos_en_word/logo.png"
# ubicacion_logo_izquierdo_del_pie_de_pagina = "src/documentos_en_word/logo_izquierdo.png"
# ubicacion_logo_derecho_del_pie_de_pagina = "src/documentos_en_word/logo_derecho.png"
ubicacion_documento_plantilla = "templates/programa_template.docx"


class Programa:
    _docentes: list[str] = []
    _campo_de_formacion: str = "Técnico Especifico - Especialidad TICs"
    _jefe_de_departamento: str = "Andrés Navarro"
    _documento: DocumentObject
    _tabla_con_datos_requeridos: Table

    def __init__(self, asignatura: str, anio_ciclo: str, carga_horaria: int):
        ubicacion_documento_plantilla_path = Path(ubicacion_documento_plantilla)
        ubicacion_documento_plantilla_path.resolve()
        self._documento = Document(ubicacion_documento_plantilla_path.as_uri())
        self._tabla_con_datos_requeridos = self._documento.tables[0]
        asignatura_en_tabla = self._tabla_con_datos_requeridos.cell(1, 1)
        asignatura_en_tabla.text = asignatura
        anio_ciclo_en_tabla = self._tabla_con_datos_requeridos.cell(2, 1)
        anio_ciclo_en_tabla.text = anio_ciclo
        campo_de_formacion_en_tabla = self._tabla_con_datos_requeridos.cell(3, 1)
        campo_de_formacion_en_tabla.text = self._campo_de_formacion
        carga_horaria_en_tabla = self._tabla_con_datos_requeridos.cell(4, 1)
        carga_horaria_en_tabla.text = f"{carga_horaria} horas cátedra"
        jefe_de_departamento_en_tabla = self._tabla_con_datos_requeridos.cell(5, 1)
        jefe_de_departamento_en_tabla.text = self._jefe_de_departamento

    def agregar_nombre_de_docentes(self, nombres: list[str]):
        self._docentes.extend(nombres)
        docentes_en_tabla = self._tabla_con_datos_requeridos.cell(6, 1)
        docentes_en_tabla.text = ", ".join(self._docentes)
        return self

    def agregar_nombre_de_docente(self, nombre: str):
        self._docentes.append(nombre)
        docentes_en_tabla = self._tabla_con_datos_requeridos.cell(6, 1)
        docentes_en_tabla.text = ", ".join(self._docentes)
        return self

    def guardar(self):
        carpeta_contenedora = Path("templates/programas")
        ubicacion_final_documento = (
            carpeta_contenedora
            / f"{self._tabla_con_datos_requeridos.cell(1, 1).text}.docx"
        )
        ubicacion_final_documento.resolve()
        self._documento.save(ubicacion_final_documento.as_uri())
        return self
